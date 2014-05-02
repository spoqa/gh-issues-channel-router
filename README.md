gh-issues-channel-router
========================

Github 이슈를 레이블 별로 나누어 동명의 Slack 채널에 전달합니다.

- [Github webhooks](http://developer.github.com/webhooks/)

How to run
==========

1. install pre-commit hook

        $ ln -s pwd/ci/pre-commit .git/hooks/

1. make virtualenv's environment.

        $ virtualenv env

1. activate environment.

        $ . env/bin/activate

1. rsolve all dependencies.

        pip install -r requirements.txt

1. run

        python app.py

