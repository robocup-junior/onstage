# RoboCupJunior OnStage

This page lists various websites, documents, posters, videos, and other resources relevant for RoboCupJunior OnStage teams, organizers
and judges. It is supposed to gather all relevant resources in one place.

If you are either organizing, running or participating in a OnStage competition and want to share your knowledge with others you
are very welcome to contribute to this page.

Find more information on how to contribute on this page: [Contribute to this page](https://robocup-junior.github.io/onstage/contribute/to_page.html).

## Build the website locally

```sh
git clone https://github.com/robocup-junior/onstage
cd onstage
pip install -r docs/requirements.txt
./docs/make.bat html
```

## Host locally
```
cd docs/_build/html
python3 -m http.server
