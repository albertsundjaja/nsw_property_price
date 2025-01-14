*This is a submission for the [GitHub Copilot Challenge ](https://dev.to/challenges/github): Fresh Starts*

## What I Built

A Vue web app that incorporates Github Model (ChatGPT-4o mini) to analyze and answer questions about NSW property data

## Demo

https://albertsundjaja.github.io/nsw_property_price/

## Repo

{% embed https://github.com/albertsundjaja/nsw_property_price %}


## Copilot Experience

This project made extensive use of Copilot help with autocomplete, edits, prompts and chat.

* Autocomplete makes writing codes faster and easier with the suggested code as I type
* Edit is pretty useful to create a scaffold for a function that I can modify to suit my specific needs
* Prompt was used to generate the download.py initial code and provide guidance on how to host my Vue JS app in github
* Chat is very useful for debugging. By entering the error logs, Copilot was able to suggest what went wrong and how to fix them

## GitHub Models

This project make use of OpenAI's GPT-4o Mini provided by [Github Models](https://github.com/marketplace/models) to analyze the NSW property prices processed data
However, model limitations of only able to take 8000 tokens input would make the response to be inaccurate as not all the data can be fed into the model for context
Only top 100 suburbs are given to the model because of reason above


## Conclusion

I have never imagined that I can make a working project in under 4 hours. AI is truly a game-changer in increasing software developers' productivity.
There is a lot to improve in this project, AI response to user's prompt will only be as accurate as the data fed into it as such it is important to ensure accurate and complete data is given to the model.