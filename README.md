# FontAwesome minify
Utilite for minifying FontAwesome for your web site.

# Description
The utility checks all HTML templates and finds used FontAwesome icons. Unused icons will be deleted.

# Using
python3 minify.py -f fontawesome.js -t templates_dir1 templates_dir2 ...
where fontawesome.js is all.js file, and templates_dir is a list of directories with HTML templates.

# Restrictions
Works only for FontAvesome 5.1 with python3.5 or older.
