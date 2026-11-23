# medsparse-playground

Run the MedSparse inference playground in your own browser. The Python launcher serves the interface on localhost. Choose a model, load its files from Hugging Face, and enter a prompt. Generation runs in a browser worker. The first model load requires internet access.

## Install and run

Requires Python 3.10 or later and a modern browser.

```sh
python -m pip install medsparse-playground
medsparse-playground
```

Use `medsparse-playground --no-browser` to print the URL and open it yourself. Press Ctrl+C in the terminal to stop the server. Model weights are downloaded separately and retain their model-card license terms. The healthcare models are for research and engineering use.

## Source

Adapted from [the AI Lab playground](https://github.com/su394611-del/su394611-del.github.io/tree/91b9714fad37ada51bd76bbb62a91b468d6ec065/playground). The packaged version points its home and privacy links to the hosted website. The original Apache 2.0 license is included.
