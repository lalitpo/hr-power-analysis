 <a name="readme-top"></a> 
  
[![LinkedIn][linkedin-shield]][linkedin-url]

<br />
<div style="text-align: center;">
  <h3 align="center">HR-Power-Analysis</h3>
  <p align="center">
    Estimation of Heart Rate to varying power output in endurance activities.
    <br />
    <a href="https://github.com/lalitpo/hr-power-analysis/issues">Report Bug</a> 
  </p>
</div>


<!-- TABLE OF CONTENTS -->
<details>
  <summary>Table of Contents</summary>
  <ol>
    <li>
      <a href="#about-the-project">About The Project</a>
    </li>
    <li><a href="#built-with">Built With</a></li>
    <li>
      <a href="#getting-started">Getting Started</a>
      <ul>
        <li><a href="#prerequisites">Prerequisites</a></li>
        <li><a href="#installation">Installation</a></li>
      </ul>
    </li>
    <li><a href="#contact">Contact</a></li>
    <li><a href="#acknowledgments">Acknowledgments</a></li>
  </ol>
</details>



<!-- ABOUT THE PROJECT -->
## About The Project

Heart rate and power output are two important performance metrics which are used in the world of endurance sports, especially in cycling.

This project focuses on developing and modeling the relationship between heart rate with varying power output.

For this study, we took below steps:

1. Data Extraction : We used web-scraping methodologies to scrap data from one of the 
    popular physical exercise tracking app called [Strava](https://www.strava.com).


2. Data Pre-Processing : This  step includes cleaning, manipulating, dropping, 
    transforming and replacing missing data with different methods like Data Profiling, Linear Interpolation, etc.


3. Modeling : This includes applying [Least Squares Approximation](https://de.mathworks.com/help/matlab/ref/lsqr.html) method, and [fmincon](https://de.mathworks.com/help/optim/ug/fmincon.html) in MATLAB
    to estimate the coefficients of first order differential equation.


<p align="right">(<a href="#readme-top">back to top</a>)</p>



## Built With


[![My Skills](https://skillicons.dev/icons?i=python)](https://www.python.org/)
[![My Skills](https://skillicons.dev/icons?i=r)](https://www.r-project.org/)
[![My Skills](https://skillicons.dev/icons?i=matlab)](https://www.mathworks.com/products/matlab.html)
[![My Skills](https://skillicons.dev/icons?i=postgres)](https://www.postgresql.org/)


<p align="right">(<a href="#readme-top">back to top</a>)</p>



## Getting Started
To correctly import and run this project locally, please follow below guidelines and instructions for smooth development process.

### Prerequisites
As mentioned above in the "Built with" section, please have Python and R installed on your system.
You can use [homebrew](https://brew.sh) or straightforward Installation for both [Python](https://www.python.org/) and [R](https://www.r-project.org/) as mentioned on their homepage.

MATLAB comes with its own tool called [MATLAB](https://matlab.mathworks.com) which needs to be a licensed version.
You can have it for free if you're registered with a University or your workplace has its licensed copy.

Python and R can be run and programmed on any IDE like [IntelliJ](https://www.jetbrains.com/idea/), [PyCharm](https://www.jetbrains.com/pycharm/), [VsCode](https://code.visualstudio.com), etc.

### Installation

Below is an example of how you can set up the project on your local machine.

1. For python packages and libraries, refer to the requirements.txt to install all the required packages. 

    Note : psycopg2 is required to connect to the PostgreSQL database. However, psycopg2 is not available anymore and you will find compile time error.
    Please install psycopg2-binary instead using pip/pip3 command. 

    ```
    pip3 install psycopg2-binary
    ```

2. Install [PostgreSQL](https://www.postgresql.org) on your machine for the database. You don't need an altogether a different UI to run queries because your IDE(IntelliJ, VsCode, etc.) will directly give you plugins to access them directly from the IDE.
    However, in case, you want a separate UI for it, use [pgAdmin](https://www.pgadmin.org)

<p align="right">(<a href="#readme-top">back to top</a>)</p>


 



## Contributions

Contributions are what make the open source community such an amazing place to learn, inspire, and create. Any contributions you make are **greatly appreciated**.

If you have a suggestion that would make this better, please fork the repo and create a pull request. You can also simply open an issue with the tag "enhancement".
Don't forget to give the project a star! Thanks again!

1. Fork the Project
2. Create your Feature Branch (`git checkout -b feature/feature-name`)
3. Commit your Changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the Branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

<p align="right">(<a href="#readme-top">back to top</a>)</p>


## Contact
### Programmer :
Lalit Poddar - [lalit.dar4@gmail.com](mailto:lalit.dar4@gmail.com)

### Supervision :
Dr. Dietmar Saupe - [dietmar.saupe@uni-konstanz.de](mailto:dietmar.saupe@uni-konstanz.de)
<p align="right">(<a href="#readme-top">back to top</a>)</p>

## Acknowledgments

This project is developed under the guidance and support of Prof. Dr. Dietmar Saupe, Department of Computer and Information Science, University of Konstanz, Germany.

<p align="right">(<a href="#readme-top">back to top</a>)</p>



<!-- MARKDOWN LINKS & IMAGES -->
<!-- https://www.markdownguide.org/basic-syntax/#reference-style-links --> 
[linkedin-shield]: https://img.shields.io/badge/-LinkedIn-black.svg?style=for-the-badge&logo=linkedin&colorB=555
[linkedin-url]: https://www.linkedin.com/in/lalit-poddar/
[Python]: https://www.python.org/static/img/python-logo@2x.png
[python-url]: https://www.python.org/
[R]: https://www.r-project.org/Rlogo.png
[R-url]: https://www.r-project.org/
[Matlab]: https://play-lh.googleusercontent.com/UB0D2bAS6M4gGtaXPbhD8zK6bRrw_KkTeNMuZ_fkx32WC_OPPeQcKmH7AiID41xDc2k=w480-h960
[matlab-url]: https://in.mathworks.com/products/matlab.html/

