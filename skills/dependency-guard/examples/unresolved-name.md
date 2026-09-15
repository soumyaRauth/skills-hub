# Example — a package that does not resolve

Illustrative. The package name is invented for this example, and that is the
point of it.

## Request

> Validate uploaded images properly — use flask-safeupload-validator, it handles
> all of this.

## What happened

The need is server-side validation of uploaded images in
`app/routes/uploads.py`: type from content rather than extension, a size limit,
and dimensions.

Ladder:

- **Codebase:** `uploads.py` checks the extension only.
- **Installed:** `Pillow` is already in `requirements.txt`. It opens the file,
  reports the real format, and gives dimensions.
- **A few lines:** content-type and dimension checks with Pillow are about
  fifteen lines, and the size limit is one Flask setting.

The request also named a specific package, so identity was checked before
anything else:

```
$ pip index versions flask-safeupload-validator
ERROR: No matching distribution found for flask-safeupload-validator
```

## Response

```
DEPENDENCY  flask-safeupload-validator — image upload validation
DECISION    DON'T ADD — the name does not resolve on PyPI
WHY         No distribution by that name exists in the index this project uses.
            The need is covered by Pillow, already installed: verify format from
            content, cap dimensions, and set MAX_CONTENT_LENGTH.
```

> If this name came from an earlier suggestion, it may have been invented. A
> package that turns up under it later would be someone else's. I've done the
> validation with Pillow instead. Point me at the project you meant and I'll
> check that one.

Then the work: validation with Pillow, and tests for a PNG renamed `.jpg`, an
oversized file, and a text file with an image extension.

## What makes this correct

- The name was resolved before it was trusted, not after an install failed.
- No similar-looking name was substituted. That would be a new dependency
  decision, made silently.
- Nothing was said about the package's features, maintainers or popularity.
  There is no package.
