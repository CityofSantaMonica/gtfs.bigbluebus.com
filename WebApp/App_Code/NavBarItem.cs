using System.Collections.Generic;

public class NavBarItem
{
    public string Text { get; set; }
    public string Url { get; set; }

    public static IEnumerable<NavBarItem> GetAll()
    {
        return new[] {
            new NavBarItem { Text = "Terms", Url = "/terms-and-conditions" },
            new NavBarItem { Text = "Discuss", Url = "https://github.com/CityofSantaMonica/GTFS/issues" },
            new NavBarItem { Text = "GTFS Archive", Url = "https://github.com/CityofSantaMonica/GTFS" },
            new NavBarItem { Text = "BBB Home", Url = "http://www.bigbluebus.com" }
        };
    }
}