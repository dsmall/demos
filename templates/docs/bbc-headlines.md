BBC News Headlines
---

--

#### News feed
The current news feed is checked every five minutes while
the application is running, or immediately if you change
the topic. The application then cycles through the top twenty stories
for that topic.


#### Weather
The location for Weather Now and the Next 3 Days is set
in the configuration file `static/public.conf`.
For example, this sets the weather location to Boston, USA:

    [Headlines]
    locationID = 4930956

To set a different location:

1. Go to the [BBC Weather home page][bbcw]
2. Enter your location in **Find a Forecast**
3. For example, choose **London**
4. On the weather page for London, look at the URL in the browser address bar, for example:

        http://www.bbc.co.uk/weather/2643743    

5. Paste the number from the end of the URL into `public.conf`:

        [Headlines]
        locationID = 2643743

6. Change from Weather Now to Next 3 Days (or vice versa) to refresh the weather information
7. You should now see the weather for your new location

<small>2 June 2013</small>

[bbcw]: http://www.bbc.co.uk/weather/

<script type="text/javascript">
    $(document).ready(function () {
        $('#doc-content a')
            .attr('target', '_blank');
    });
</script>
