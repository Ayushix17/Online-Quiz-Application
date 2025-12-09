# lib Folder

This folder contains external libraries and dependencies for the Online Quiz Application.

## Structure

- **Third-party JARs**: Place any external Java libraries (.jar files) here
- **Database drivers**: JDBC drivers for database connectivity
- **Utilities**: Helper libraries and tools

## Adding Dependencies

1. Download the required `.jar` file
2. Place it in this folder
3. Add it to your classpath when compiling/running:

```bash
javac -cp lib/*:. *.java
java -cp lib/*:. Main
```

## Current Dependencies

Add your dependencies here as you add them to the project.
