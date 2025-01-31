git hooks for Jupyter

add these to your `.git/hooks`

For now, we just have `post-checkout` and `post-merge`,
both of which attempt to rebuild javascript and css sourcemaps,
so make sure that you have a fully synced repo whenever you checkout or pull.

To use these hooks, run `./install-hooks.sh`.
