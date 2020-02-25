# Transitioning from Jupyter Notebook to Jupyter Server.

**A story about configuration**

Steps to handling traits during a "Transition and Deprecation Period".

1. If the argument is prefixed with `ServerApp`, pass this trait to `ServerApp`.
2. If the argument is prefixed with `NotebookApp`,
    - If the argument is a trait of `NotebookApp` *and* `ServerApp`:
        1. Raise a warning—**for the extension developers**—that there's redundant traits.
        2. Pass trait to `NotebookApp`.
    - If the argument is a trait of just `ServerApp` only (i.e. the trait moved from `NotebookApp` to `ServerApp`):
        1. Raise a `"DeprecationWarning: this trait has moved"` **for the user**.
        2. Migrate/write the trait to a new config file if it came from a config file.
        3. Pass trait to `ServerApp`.
    - If the argument is a trait of `NotebookApp` only, pass trait to `NotebookApp`.
    - If the argument is not found in any object, raise a `"Trait not found."` error.
3. If the argument is prefixed with `ExtensionApp`:
    - If the argument is a trait of `ExtensionApp` and either `NotebookApp` or `ServerApp`,
        1. Raise a warning—**for the extension developers**—that there's redundant traits.
        2. Pass trait to Step 2 above.
    - If the argument is *not* a trait of `ExtensionApp`, but *is* a trait of either `NotebookApp` or `ServerApp` (i.e. the trait moved from `ExtensionApp` to `NotebookApp`/`ServerApp`):
        1. Raise a `"DeprecationWarning: this trait has moved"` **for the user**.
        2. Migrate/write the trait to a new config file if it came from a config file.
        2. Pass trait to Step 2 above.
    - If the argument is *not* a trait of `ExtensionApp` and not a trait of either `NotebookApp` or `ServerApp`, raise a `"Trait not found."` error.
