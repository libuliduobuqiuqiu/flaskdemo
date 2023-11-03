# coding: utf-8
"""
    :date: 2023-11-2
    :author: linshukai
    :description: About Start flasker service
"""

from flasker import create_app



if __name__ == "__main__":
    app = create_app()
    app.run("127.0.0.1", port=8992)