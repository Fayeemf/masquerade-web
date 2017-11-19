# Masquerade Web

Open-source engine behind the Many Masqs blog.

Templating using the `template.blog` file.

Examples provided in `blogs/example.blog.example` and `blog/example.html`.

## Usage:

1. Make a blog post using our flavor of markdown. Place this into `blogs/<filename>.blog`.

2. Run `python main.py` to generate blogs.

(Or set up a git hook on your machine that runs this command whenever you commit, then adds all the created files and commits them as well. One hook may be `./.git/hooks/pre-commit`, with the SHEBANG and `python main.py && git add --all`.)

## Credits

`CodePen` for making it easy to find good HTML.