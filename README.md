# How to Assess Measurement Capabilities of a Security Monitoring Infrastructure and Plan Investment through a Graph-based Approach

## Abstract

Security monitoring is one of the most critical activities while managing cyber security for every organization, as it is one of the first in different security processes and systems (e.g., risk identification and threat detection). To correctly monitor the current situation and support the decision-making process, companies need to collect heterogeneous data and compute security metrics that provide a quantitative evaluation. In this paper, we address the problem of supporting security experts in managing security metrics efficiently and effectively by considering the trade-off cost-benefit between the usage of a particular monitoring tool and the benefit of including it in the monitoring infrastructure. To this aim, we introduce the concept of Metric Graph Model (MGM) and we leverage it to solve a set of identified security monitoring problems. We prove the NP hardness of some of these problems and in such cases, we propose heuristics for solving them based on the MGM. We provide a performance evaluation of the proposed heuristics through synthetic MGMs and finally, we present a usage scenario based on an instance of the MGM derived from a state-of-the-art security metric taxono

## Introduction

This project is centered around the development of the MGM (Metric Graph Model), a model that abstracts the concepts of security metrics and their implementability. In the MGM graph, nodes represent security metrics, clusters, inputs, and sources. This structure allows for the construction of a security metric through a defined sequence. We have formally addressed the first problem associated with improving security awareness, termed *implementability*. A security metric is deemed implementable if it is linked to one or more sources that facilitate its implementation.

## Getting Started

To get started with the MGM project, you'll first need to install the required dependencies and then run the web application. Follow the steps below to set up the project on your local machine.

### Prerequisites

Before you can run the project, make sure you have Python installed on your system. This project has been tested on Python 3.8 and above. You can download Python from [the official website](https://www.python.org/downloads/).

### Installing Dependencies

1. Navigate to the project directory: cd Metric-Management-Graph
2. Install the required Python dependencies: pip install -r requirements.txt


This will start the web application on your local machine. You can access it by visiting `http://localhost:5000` in your web browser.

## Contributing

Contributions to the MGM project are welcome. If you wish to contribute, please fork the repository and submit a pull request.



