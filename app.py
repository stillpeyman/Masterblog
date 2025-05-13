import json
from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)


def load_posts():
    try:
        with open('blog_posts.json', 'r', encoding='utf-8') as handle:
            return json.load(handle)
    except FileNotFoundError:
        # Return empty list if file not existing
        return []


@app.route('/')
def index():
    blog_posts = load_posts()
    return render_template('index.html', posts=blog_posts)


@app.route('/add', methods=['GET', 'POST'])
def add():
    # Handle POST request
    if request.method == 'POST':
        author = request.form.get('author')
        title = request.form.get('title')
        content = request.form.get('content')

        blog_posts = load_posts()
        new_id = len(blog_posts) + 1

        new_post = {
            'id': new_id,
            'author': author,
            'title': title,
            'content': content,
            'likes': 0
        }

        blog_posts.append(new_post)

        with open('blog_posts.json', 'w', encoding='utf-8') as handle:
            json.dump(blog_posts, handle, indent=4)

        return redirect(url_for('index'))

    # GET request: render <add.html> form
    return render_template('add.html')


@app.route('/delete/<int:post_id>')
def delete(post_id):
    blog_posts = load_posts()

    # List comprehension more concise and safer way to filter a list
    blog_posts = [post for post in blog_posts if post['id'] != post_id]

    # Reassign IDs to maintain sequential order, starting from 1
    for i, post in enumerate(blog_posts, start=1):
        post['id'] = i

    with open('blog_posts.json', 'w', encoding='utf-8') as handle:
        json.dump(blog_posts, handle, indent=4)

    return redirect(url_for('index'))


@app.route('/update/<int:post_id>', methods=['GET', 'POST'])
def update(post_id):
    blog_posts = load_posts()

    # Fetch blog post with matching ID from JSON file
    post_to_update = next((post for post in blog_posts if post['id'] == post_id), None)
    if post_to_update is None:
        return "Post not found", 404

    if request.method == 'POST':
        # Update the post's fields from form data
        post_to_update['author'] = request.form.get('author')
        post_to_update['title'] = request.form.get('title')
        post_to_update['content'] = request.form.get('content')

        # Save updated blog_posts list back to JSON file
        with open('blog_posts.json', 'w', encoding='utf-8') as handle:
            json.dump(blog_posts, handle, indent=4)

        return redirect(url_for('index'))

    # GET request: render <update.html> form
    return render_template('update.html', post=post_to_update)


@app.route('/likes/<int:post_id>', methods=['POST'])
def like(post_id):
    blog_posts = load_posts()

    for post in blog_posts:
        if post['id'] == post_id:
            # Increment the likes count
            post['likes'] = post.get('likes', 0) + 1
            break
    else:
        return "Post not found", 404

    # Save updated blog_posts list back to JSON file
    with open('blog_posts.json', 'w', encoding='utf-8') as handle:
        json.dump(blog_posts, handle, indent=4)

    return redirect(url_for('index'))


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5001, debug=True)


