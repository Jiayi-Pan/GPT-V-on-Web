# [🧠GPT-4 Vision](https://openai.com/research/gpt-4v-system-card) x [⌨️Vimium](https://github.com/philc/vimium) = Autonomous Web Agent

This project leverages GPT4V to create an autonomous / interactive web agent. The action space are discretized by [Vimium](https://github.com/philc/vimium).

It's a fun project to explore the possibility of using GPT-4V to interact with the web, but do not meant to be a serious project at current stage.

## Get Started
**Install**
```bash
# For Mac users
brew install chromedriver  
# run `brew upgrade chromedriver` if you already have it
pip install git+https://github.com/Jiayi-Pan/WebAI.git
```

**Run**
```bash
webai --start_link "https://www.google.com"
```
## Related Works
- [GPT-4V-Act](https://github.com/ddupont808/GPT-4V-Act)