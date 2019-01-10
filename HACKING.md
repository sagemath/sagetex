To create a new release
  1. assuming this repo is checked out already.
  1. bump up the version in setup.py and in 2 places in sagetex.dtx: the macro \ST@ver and inside
     `<*latex|python>` few lines above.
  1. run `make` with `sage` in the `PATH`, it should run without errors, and produce sagetex.pdf and example.pdf
  1. commit and push
  1. run `make dist` to create a tarball in `dist/`
  1. On github, make a new release, appropriately tagged, add there binary assets: the tarball from `dist/` and the pdf files
     as above
  1. At this point, you are set to create Sage ticket to update the package, giving the tarball link you added as an asset.
  1. Copy the tarball to `SAGEROOT/upstream/`, update the checksum, create a trac git branch, etc., test that the
     installation of Sage package sagetex works, etc.
