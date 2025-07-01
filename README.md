# Corabits Univers Asset Manager

Simple asset manager that allows to upload files into bucketts, and retrieve them later.

Basic goals:

- [x] Create buckets
- [x] Upload files
- [x] Retrieve files
- [x] Delete files
- [x] List files
- [x] Initial backend is always disk.

Future goals:

- [ ] Filters - At upload do some operations via config, like resize, convert, reencode...
- [ ] Related files - Using the filters have alternate views of the file, as the reencoded, or a given cropped size of an image.
- [ ] File versioning - Allow to keep multiple versions of the same file, and retrieve them later.
- [ ] Alternative backends - S3, GCP, Azure, etc. Each bucket can have other backend.
