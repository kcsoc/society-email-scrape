# society-email-scrape

## Site Live at https://kcsoc.github.io/society-email-scrape/

## How to automatically generate new data

- Go to `unis.yml`
- Add your uni
- Create a Pull Request
- GitHub Actions bot will automatically update as per your PR
- When I approve the PR your Uni will automatically be loaded into the website
- https://kcsoc.github.io/society-email-scrape/

## How to run yourself

Add any URLs to `unis.yml`

PS: Don't forget to leave a trailing newline at the end of the file

```bash
git clone https://github.com/kcsoc/society-email-scrape.git
cd society-email-scrape
./main.sh
```

## How to test for a single university

1. Choose a university (on your own or from unis.yml)
1. Run `python main.py UNIVERSITY_URL`


## To run with debug mode

The program features a debug mode. To enable it, simply preface the python command with `DEBUG_MODE=true`

For example:
```bash
DEBUG_MODE=true python3 main.py https://www.imperialcollegeunion.org/activities/a-to-z
```

Or set the `DEBUG_MODE` variable to true globally in your shell with, `export DEBUG_MODE=true`

Note: `DEBUG_MODE` is enabled when the variable is set, to unset, use the `unset` keyword in bash
