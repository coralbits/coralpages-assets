# Coralpages Assets

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

## Simple web app

There is a simple web app running at `/` to allow easy access to items. It can be disabled at the `config.yaml` file.

## Manual test

Create a bucket

```sh
curl -X PUT http://localhost:8005/test/
```

Upload a file

```sh
curl -T test.txt http://localhost:8005/test/test.txt
```

List files

```sh
curl http://localhost:8005/test/
```

Retrieve a file

```sh
curl http://localhost:8005/test/test.txt
```

Delete a file

```sh
curl -X DELETE http://localhost:8005/test/test.txt
```
