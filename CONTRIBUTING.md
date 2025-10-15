# Contributing

## Introduction

We appreciate your interest in considering contributing to valkey-py.
Community contributions mean a lot to us.

## Contributions we need

You may already know how you'd like to contribute, whether it's a fix for a bug you
encountered, or a new feature your team wants to use.

If you don't know where to start, consider improving
documentation, bug triaging, and writing tutorials are all examples of
helpful contributions that mean less work for you.

## Developer Certificate of Origin

We respect the intellectual property rights of others and we want to make sure
all incoming contributions are correctly attributed and licensed. A Developer
Certificate of Origin (DCO) is a lightweight mechanism to do that. The DCO is
a declaration attached to every commit. In the commit message of the contribution,
the developer simply adds a `Signed-off-by` statement and thereby agrees to the DCO,
which you can find below or at [DeveloperCertificate.org](http://developercertificate.org/).

```text
Developer's Certificate of Origin 1.1

By making a contribution to this project, I certify that:

(a) The contribution was created in whole or in part by me and I
    have the right to submit it under the open source license
    indicated in the file; or

(b) The contribution is based upon previous work that, to the
    best of my knowledge, is covered under an appropriate open
    source license and I have the right under that license to
    submit that work with modifications, whether created in whole
    or in part by me, under the same open source license (unless
    I am permitted to submit under a different license), as
    Indicated in the file; or

(c) The contribution was provided directly to me by some other
    person who certified (a), (b) or (c) and I have not modified
    it.

(d) I understand and agree that this project and the contribution
    are public and that a record of the contribution (including
    all personal information I submit with it, including my
    sign-off) is maintained indefinitely and may be redistributed
    consistent with this project or the open source license(s)
    involved.
```

We require that every contribution to Valkey to be signed with a DCO. We require the
usage of known identity (such as a real or preferred name). We do not accept anonymous
contributors nor those utilizing pseudonyms. A DCO signed commit will contain a line like:


```text
Signed-off-by: Jane Smith <jane.smith@email.com>
```

You may type this line on your own when writing your commit messages. However, if your
user.name and user.email are set in your git configs, you can use `git commit` with `-s`
or `--signoff` to add the `Signed-off-by` line to the end of the commit message. We also
require revert commits to include a DCO.

If you're contributing code to the Valkey project in any other form, including
sending a code fragment or patch via private email or public discussion groups,
you need to ensure that the contribution is in accordance with the DCO.

## Your First Contribution

Unsure where to begin contributing? You can start by looking through
[help-wanted
issues](https://github.com/valkey-io/valkey-py/issues?q=is%3Aopen+is%3Aissue+label%3ahelp-wanted).

Never contributed to open source before? Here are a couple of friendly
tutorials:

-   <http://makeapullrequest.com/>
-   <http://www.firsttimersonly.com/>

## Getting Started

Here's how to get started with your code contribution:

1.  Create your own fork of valkey-py
2.  Do the changes in your fork
3.
    *Create a virtualenv and install the development dependencies from the dev group:*

        a.  python -m venv .venv
        b.  source .venv/bin/activate
        c.  pip install --group dev

4.  If you need a development environment, run `invoke devenv`. Note: this relies on docker compose to build environments, and assumes that you have a version supporting [docker profiles](https://docs.docker.com/compose/profiles/).
5.  While developing, make sure the tests pass by running `invoke tests`
6.  If you like the change and think the project could use it, send a
    pull request

To see what else is part of the automation, run `invoke -l`

## The Development Environment

Running `invoke devenv` starts all of the dockers used by this
project, and leaves them running. These can be easily cleaned up with
`invoke clean`. NOTE: it is assumed that the user running these tests,
can execute docker and its various commands.

-   A master Valkey node
-   A Valkey replica node
-   Three sentinel Valkey nodes
-   A valkey cluster
-   An stunnel docker, fronting the master Valkey node

The replica node, is a replica of the master node, using the
[leader-follower replication](https://redis.io/topics/replication)
feature.

The sentinels monitor the master node in a [sentinel high-availability
configuration](https://redis.io/topics/sentinel).

## Testing

Call `invoke tests` to run all tests, or `invoke all-tests` to run linters
tests as well. With the 'tests' and 'all-tests' targets, all Valkey and
ValkeyCluster tests will be run.

It is possible to run only Valkey client tests (with cluster mode disabled) by
using `invoke standalone-tests`; similarly, ValkeyCluster tests can be run by using
`invoke cluster-tests`.

Each run of tests starts and stops the various dockers required. Sometimes
things get stuck, an `invoke clean` can help.

## Documentation

If relevant, update the code documentation, via docstrings, or in `/docs`.

You can check how the documentation looks locally by running `invoke build-docs`
and loading the generated HTML files in a browser.

Historically there is a mix of styles in the docstrings, but the preferred way
of documenting code is by applying the
[Google style](https://sphinxcontrib-napoleon.readthedocs.io/en/latest/example_google.html).
Type hints should be added according to PEP484, and should not be repeated in
the docstrings.

### Docker Tips

Following are a few tips that can help you work with the Docker-based
development environment.

To get a bash shell inside of a container:

`$ docker run -it <service> /bin/bash`

Containers run a minimal Debian image that probably lacks tools you want
to use. To install packages, first get a bash session (see previous tip)
and then run:

`$ apt update && apt install <package>`

You can see the logging output of a containers like this:

`$ docker logs -f <service>`

### Troubleshooting

If you get any errors when running `make dev` or `make test`, make sure
that you are using supported versions of Docker.

Please try at least versions of Docker.

-   Docker 19.03.12

## How to Report a Bug


### Security Vulnerabilities

Reporting a vulnerability? See [SECURITY.md](https://github.com/valkey-io/valkey-py/blob/main/SECURITY.md).

### Everything Else

When filing an issue, make sure to answer these five questions:

1.  What version of valkey-py are you using?
2.  What version of valkey are you using?
3.  What did you do?
4.  What did you expect to see?
5.  What did you see instead?

## Suggest a feature or enhancement

If you'd like to contribute a new feature, make sure you check our
issue list to see if someone has already proposed it. Work may already
be underway on the feature you want or we may have rejected a
feature like it already.

If you don't see anything, open a new issue that describes the feature
you would like and how it should work.

## Code review process

The core team regularly looks at pull requests. We will provide
feedback as soon as possible. After receiving our feedback, please respond
within two weeks. After that time, we may close your PR if it isn't
showing any activity.
