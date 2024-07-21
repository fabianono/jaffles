<h1>Project Jaffles!</h1>

<p>My first data injestion pipeline project from an <a href = "https://github.com/dbt-labs/jaffle-shop">online repository by DBT</a>( <span style = "font-size:12px">please be nice &#x1F60A;</span>). The original cloned repository can be found under "<a href = "https://github.com/fabianono/jaffles/tree/main/deprecated_jaffleshop_dbt">deprecated_jaffleshop_dbt</a>". The data injestion scripts can be found under the folder "<a href = "https://github.com/fabianono/jaffles/tree/main/PipelineInjestionScripts">PipelineInjestionScripts"</a>".</p>

<div style = "margin-bottom:16px;">
Here is a snapshot of the data mapping.
<img src = "https://github.com/fabianono/jaffles/blob/main/JaffleShop_MappingDiagram.drawio.png">
</div>

<div style = "font-size:12px;">Some notes:
<ul>
    <li>This is my first attempt at data injestion and it is very basic. My codes could probably be much more efficient and the code architecture could probably also be better.
    <li>The data injestion was designed to be connected to Google cloud. However, I am on the free tier so by the time this project is live, the free tier would have probably expired and I would have shut down the GCP server.
    <li>The data created was through the use of a python tool by DBT called jafgen which generates datasets for the Jaffleshop project.
    <li>The data injestion is only for 3 years as I had concerns about the storage limit of the GCP server to remain in the free tier.
<ul>
</div>