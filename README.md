blog
----

This is [my personal blog](https://fohlen.dev) which is built using [Hugo](https://gohugo.io) - thanks to them for making static websites so awesome.

You can get started as such:

```shell
brew install hugo
hugo server
```

If you want to run the notebooks accompanying the experiments in the blog, install the dependencies via:

```
brew install uv
uv sync
./scripts/install-git-filters.sh
```

This should allow to rerun all notebooks.