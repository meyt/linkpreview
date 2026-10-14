# Contributing

## Commit messages

This project uses [Conventional Commits](https://www.conventionalcommits.org/):

```
<type>(optional scope): <description>
```

Common types: `feat`, `fix`, `docs`, `test`, `refactor`, `chore`.
Mark breaking changes with `!` (e.g. `feat!: ...`) or a `BREAKING CHANGE:` footer.

Examples:

```
feat: add allow_private option
fix: use python3.8 compatible type annotation
chore: add makefile
```

## Development

```sh
make install
make test
```
