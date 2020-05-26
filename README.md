# Data Challenge Project

## About

In this project, we operate as a digital consultancy looking to help out YouTubers. We have gathered rigorous statistical research notebooks under the Research folder, and have provided actionable insights under the Insights folder. Of particular interest is the <code>Main Insights</code> file.

## Getting Started

Save the <code>youtube-new</code> directory containing the relevant <code>.csv</code> and <code>.json</code> files into the <code>data</code> directory. Then run <code>python prepare_data.py</code> to clean and feature engineer the data.

The <code>colourdata</code> directory generates a <code>colour-output.csv</code> file for use in the main insights notebook. Again, we require that the <code>youtube-new</code> directory be saved in the same directory. The correct order of commands to generate the <code>.csv</code> file is <code>python generate_colour.py</code> then <code>python process_colour.py</code> though it is recommended that you do not run this and instead use the already generated <code>csv</code> file since doing so saves a lot of time.

The <code>Main Insights</code> notebook aims at reflecting the kind of business that this project could develop into and is our main deliverable. The various research notebooks support this work and are held to a high standard of rigor. 

We have also included the archived EDA files though these are no longer functional and are only included for the sake of completeness.

## Dependencies

Install dependencies from requirements.txt

## Authors

Ramin Tawab, Oliver Batey, Alexander Marwan Farha, Matthew Nally
