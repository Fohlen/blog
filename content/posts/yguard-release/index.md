---
title: "yGuard is now open source - obfuscation easy as pie"
description: "yGuard, a Java bytecode obfuscation and shrinking tool, has been released openly, thanks to a joint effort with yWorks."
author: "Lennard Berger"
date: "2020-01-08"
categories: [java,oss,obfuscation]
---

**Disclaimer: This is not a sponsored post**

I work for a company called [yWorks](https://yworks.com). They make [libraries for graphs](https://www.yworks.com/products/yfiles) that are (imho) state of the art, and also are a fun company to work at 🍺

Because these libraries are sophisticated the company is very inclined to protect their intellectual property. In the golden age of Java (which was right about the time they put this onto the market) it would have been crucial to implement some sorts of protection in order to ensure this IP. This is why `yGuard` was initially developed (side note: when I first touched the repository, some assets were as old as 11 years).

I love open source - period. Knowing this, [Sebastian Müller](https://github.com/yGuy) approached me a while ago, certain I would be 🔥 for making this product available for a wider audience. We had a brief discussion and off I went on my journey to make it open-source.

I made a checklist of things that needed to be addressed before releasing it to the public on GitHub:

- [x] relicense everything that can be relicensed
- [x] replace proprietary code with libraries or rewrite it if necessary
- [x] replace ancient build system and dependencies with up-to-date ones
- [x] set up tests and CI so it stays in good shape
- [x] add extensive documentation and sample code
- [x] add contribution guidelines

With this list done, I'm thrilled to announce: we released [yGuard](https://github.com/yWorks/yGuard/) into the wild (a while ago)!

This post however should not only be a mere release announcement, but I am going to put some sample code here, so it becomes clear what this obfuscation actually does 💡

Say, we have a rather complete Java application that has an entrypoint like so:

```java
package com.yworks.example;

public class HelloWorld {
    public static void main(String[] args) {
        System.out.println("Hello World");
    }
}
```

Now, given we use `Gradle` as our build system, we could use a very simple `yguard` task to obfuscate the resulting `.jar`

```gradle
task obfuscate {
  dependsOn jar

  doLast {
    ant.taskdef(
            name: 'yguard',
            classname: 'com.yworks.yguard.YGuardTask',
            classpath: sourceSets.main.runtimeClasspath.asPath
    )

    def archivePath = jar.archiveFile.get().asFile.path
    ant.yguard {
      inoutpair(in: archivePath, out: archivePath.replace(".jar", "_obf.jar"))
      shrink(logfile: "${buildDir}/yshrink.log.xml") {
        keep {
          method(name: "void main(java.lang.String[])", "class": application.mainClassName)
        }
      }
      rename(mainclass: application.mainClassName, logfile: "${buildDir}/yguard.log.xml") {
        property(name: "error-checking", value: "pedantic")
      }
    }
  }
}
```

This tells the build system:

1. configure an `Ant` task so we can use `yguard`
2. execute the `yguard` task with an input and output `.jar` 
3. shrink the resulting `.jar`, leaving only classes and methods that are loaded from `main`
4. obfuscate **all** class names, function names, variable names, ... **except** for `main`

Once we call `gradle obfuscate` this will produce an obfuscated `.jar`, leaving nothing but a weird trail of characters in the file names and classes.

Did you notice the `logfile` property? This is the best part. We can use the mapping established during obfuscation to unscramble stacktraces!

I could write a rather lengthy article about all the possible configurations that you can use, which would far exceed a simple introduction. For a more thorough explanation, please have a look at the [extensive documentation](https://yworks.github.io/yGuard/) and [examples](https://github.com/yWorks/yGuard/tree/master/examples), which covers all of these options.
