# Convid19 data

Data processing from Johns Hopkins University.

Original data: [link](https://github.com/CSSEGISandData/COVID-19)

## Docker

Create SSH keys with `ssh-keygen -t rsa -b 4096 -C "your-email@here"` and set it up in GitHub.

Use the script below to update the data.

```shell
$ docker build covid19-data . && docker run --rm \
-e PRIVATE_KEY="$(cat ~/.ssh/id_rsa)" \
-e PUBLIC_KEY="$(cat ~/.ssh/id_rsa.pub)" \
-e USER_NAME="Your Name" \
-e USER_EMAIL="your-email@here" \
-e REPOSITORY="your/repository" \
covid19-data
```