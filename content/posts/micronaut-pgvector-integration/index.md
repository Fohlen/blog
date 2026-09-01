---
title: "Micronaut Data and pgvector"
description: "How to retrieve vector data from Postgres using Micronaut Data"
author: "Lennard Berger"
date: "2025-03-17"
categories: [java,micronaut,data,jdbc,postgres,pgvector,word embeddings]
---

Recently [vector embeddings](https://www.elastic.co/what-is/vector-embedding) have been all the rage. Vector embeddings are a way to project data (usually text data such as words and sentences) into a dense vector representation of a fixed size.
This could be useful in natural language processing, where you want to build a retrieval augmented generation pipeline. It could be useful in object character recognition, if you want to convert your document into a searchable representation etc.

Vector embeddings have seen a lot of popularity among the NoSQL crowd. I already linked [ElasticSearch](https://www.elastic.co/elasticsearch), which has a vector search feature. The self-proclaimed forerunner is [QDrant](https://qdrant.tech), which is also very useful.
What do both of these databases have in common? They are shiny, they're new, and they are document-based datastores.

Many of us however prefer structured databases, as in SQL. Luckily, Postgres is an epic database, has support for vectors via the [pgvector extension](https://github.com/pgvector/pgvector).

This blog post will show a viable recipe of how to integrate `pgvector` into your project using nothing but [JDBC](https://jdbc.postgresql.org) and the standard support via [Micronaut Data](https://micronaut-projects.github.io/micronaut-data/latest/guide/).
It may be applicable beyond Micronaut, as the converters are also part of Spring and Quarkus, but I am not covering their support here.

# Getting started

We'll follow along the [Micronaut Data and Java](https://guides.micronaut.io/latest/micronaut-java-records-maven-java.html#getting-started) records feature but omit some steps where it doesn't closely align with the goal of this guide.

As a very first step we need to initialize Micronaut Data with Postgres and JDBC:

```bash
mn create-app --jdk=17 \
   example.micronaut.micronautguide \
   --features=data-jdbc,postgres,liquibase \
   --build=maven \
   --lang=java \
```

After initialising our project, we'll want to create a table holding our embedding. For this, we'll create a Liquibase changelog:

```yaml
databaseChangeLog:
  - changeSet:
      id: 1
      author: Lennard Berger
      changes:
        - createTable:
            columns:
              - column:
                  constraints:
                    nullable: false
                    primaryKey: true
                    primaryKeyName: embedding_pkey
                  type: VARCHAR(255)
                  name: key
              - column:
                  constraints:
                    nullable: false
                  type: VECTOR(512)
                  name: value
              - column:
                  constraints:
                    nullable: false
                  name: created
                  type: TIMESTAMP WITHOUT TIME ZONE
            tableName: embedding
```

We create an embedding column with a primary key named key, a creation time stamp, and a vector column of size 512. You'll need to adjust this table to your needs appropriately. Save this file under `src/main/resources/db/01-add-embedding.yml` and adjust the main changelog, then run your Liquibase migrations against the database.

The next step is to create a class which maps our table to an entity, which we will call the embedding class:

```java
package example.micronaut.micronautguide;

import example.micronaut.micronautguide.Vector;
import io.micronaut.core.annotation.NonNull;
import io.micronaut.data.annotation.DateCreated;
import io.micronaut.data.annotation.Id;
import io.micronaut.data.annotation.MappedEntity;
import jakarta.validation.constraints.NotBlank;
import java.time.Instant;

/**
 * Represents an embedding in the embeddings table
 *
 * @param key     - the key this embedding is associated to
 * @param value   - the embedding
 * @param created - when the embedding was computed
 */
@MappedEntity
public record Embedding(
    @Id @NonNull @NotBlank String key,
    @NonNull @NotBlank Vector value,
    @DateCreated @NonNull @NotBlank Instant created
) {

}
```

As you can see I have chosen to represent the data of the vector to be represented by a `Vector` class. Consequently we follow with a definition of a vector:

```java
package example.micronaut.micronautguide;

import io.micronaut.data.annotation.TypeDef;
import io.micronaut.data.model.DataType;

@TypeDef(type = DataType.OBJECT)
public class Vector {

  private final double[] value;

  private Vector(double[] value) {
    this.value = value;
  }

  public static Vector valueOf(double[] value) {
    return new Vector(value);
  }

  public double[] getValue() {
    return value;
  }

}
```

Given the entity and representation of the vector, we need to tell Micronaut how to convert our custom object into SQL.

## Converting vectors

To be able to convert objects from JDBC to our custom Vector class we will implement a `PGObjectToVectorConverter`, converting `PGObject` (coming from JDBC):

```java
package example.micronaut.micronautguide;

import io.micronaut.core.convert.ConversionContext;
import io.micronaut.core.convert.TypeConverter;
import jakarta.inject.Singleton;
import java.util.Arrays;
import java.util.Optional;
import org.postgresql.util.PGobject;

@Singleton
public class PGObjectToVectorConverter implements TypeConverter<PGobject, Vector> {

  @Override
  public Optional<Vector> convert(PGobject object, Class<Vector> targetType) {
    if (object.isNull()) {
      return Optional.empty();
    } else {
      String vector = object.getValue();

      return Optional.of(Vector.valueOf(Arrays.stream(
          vector.substring(1, vector.length() - 1).split(",")
      ).mapToDouble(Double::parseDouble).toArray()));
    }
  }

  @Override
  public Optional<Vector> convert(PGobject object, Class<Vector> targetType,
      ConversionContext context) {
    return convert(object, targetType);
  }
}
```

Since we want this relationship to be bidirectional, we will also implement a `VectorToPGObjectConverter` class:

```java
package example.micronaut.micronautguide;

import io.micronaut.core.convert.ConversionContext;
import io.micronaut.core.convert.TypeConverter;
import jakarta.inject.Singleton;
import java.sql.SQLException;
import java.util.Arrays;
import java.util.Optional;
import org.postgresql.util.PGobject;

@Singleton
public class VectorToPGObjectConverter implements TypeConverter<Vector, PGobject> {

  @Override
  public Optional<PGobject> convert(Vector object, Class<PGobject> targetType) {
    if (object == null) {
      return Optional.empty();
    } else {
      PGobject pgObject = new PGobject();
      pgObject.setType("vector");
      try {
        pgObject.setValue(Arrays.toString(object.getValue()));
        return Optional.of(pgObject);
      } catch (SQLException e) {
        throw new RuntimeException(e);
      }
    }
  }

  @Override
  public Optional<PGobject> convert(Vector object, Class<PGobject> targetType,
      ConversionContext context) {
    return convert(object, targetType);
  }
}
```

The next step is to implement a repository and to actually access our embeddings.

## Accessing the data

In order to access our data we need to implement a corresponding repository. This step is very straightforward:

```java
package example.micronaut.micronautguide;


import example.micronaut.micronautguide.Vector;
import example.micronaut.micronautguide.Embedding;
import io.micronaut.data.annotation.Query;
import io.micronaut.data.jdbc.annotation.JdbcRepository;
import io.micronaut.data.model.query.builder.sql.Dialect;
import io.micronaut.data.repository.CrudRepository;
import java.util.Collection;
import java.util.List;
import org.postgresql.util.PGobject;

@JdbcRepository(dialect = Dialect.POSTGRES)
public interface EmbeddingRepository extends CrudRepository<Embedding, String> {

  @Query("SELECT AVG(e.value) FROM Embedding e WHERE e.key IN (:keys)")
  Vector averageForKeys(Collection<String> keys);

}
```

In an controller we can now depend on the `EmbeddingRepository` and query individual embeddings. 
We can use the full array of [available functions](https://github.com/pgvector/pgvector#querying).

## Querying by vector

So far we covered the process of exporting a vector out of Postgres into our Micronaut application. In some cases we want to do the reverse. Consider the following function definition:

```java
  @Query("SELECT e.key FROM Embedding e ORDER BY :vector <-> e.value LIMIT :limit")
  List<String> queryKeysForValue(Vector vector, int limit);
```

Unfortunately, querying by object type isn't readily supported in Micronaut data. One way to hack around this limitation is to convert Vector instances back to `PGObject`, like so:

```java
  @Query("SELECT e.key FROM Embedding e ORDER BY :vector <-> e.value LIMIT :limit")
  List<String> queryKeysForValue(PGobject vector, int limit);
```

In our controller, we can use the `VectorToPGObjectConverter` to accomplish this:

```java
VectorToPGObjectConverter converter = new VectorToPGObjectConverter();
Optional<PGobject> vectorObject = converter.convert(myEmbedding, PGobject.class);
```

This object can then be passed to `queryKysForValue`, e.g `repository.queryKeysForValue(vectorObject.get())`.

## Indexing the data

If you want to perform similarity lookups, such as the `queryKeysForValue` method, it is a good idea to create an index for your data. 
The trade-offs of index types [are discussed in the pgvector documentation](https://github.com/pgvector/pgvector?tab=readme-ov-file). For simplicity we'll use a standard HNSW index in this example. Your Liquibase config may look this:

```yaml
databaseChangeLog:
  - changeSet:
      id: 2
      author: Lennard Berger
      changes:
        - sql:
            dbms: postgresql
            sql: CREATE INDEX embedding_value_idx ON embedding USING hnsw (value);
      rollback:
        - sql:
            dbms: postgresql
            sql: DROP INDEX embedding_value_idx
```

Bear in mind, creating indexes can put considerable resource constraints on your database for the time being.

## A note about LangChain4J

If instead of a similarity search platform we wanted to build a fully-fledged retrieval-augmented generation pipeline, it may be worthwhile to explore [LangChain4J](https://micronaut-projects.github.io/micronaut-langchain4j/latest/guide/).
According to the documentation they have support for `pgvector` built in, and one only needs to configure their datasource like so:

```yaml
datasources.default.dialect: postgres
langchain4j.pgvector.embedding-stores.default.table: "mytable"
langchain4j.pgvector.embedding-stores.default.dimension: 384

# Add this if you plan to use testresources
test-resources.containers.postgres.image-name: pgvector/pgvector:pg16
```

However, you will loose a lot of introspection. If LangChain4J doesn't exactly cover your use case, this solution is probably sub-optimal.

## Closing remarks

PostgreSQL is an excellent database which stands the test of time remarkably well. It can operate at gigabyte to terrabyte scale relatively easily. If you're using Spanner, it scales to even larger use-cases.
`pgvector` is a very welcome companion to the core extensions. It is well thought-out, reliable and scaleable.

Since it is not part of the core extensions (unfortunately), tooling in third-party applications can be poor. This blog shows how we can use JDBC to leverage the power of `pgvector` regardless. It should be applicable to a wide range of frameworks (Quarkus, Spring Data etc) beyond Micronaut.

If you do discover how to transiently convert object-type data in Micronaut Data directly (without casting to PGObject), please do let me know, so this blog post can be ammended.
