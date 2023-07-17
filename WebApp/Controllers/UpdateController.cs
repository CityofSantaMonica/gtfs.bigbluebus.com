using System.IO;
using System.Linq;
using System.Net;
using System.Web;
using System.Web.Http;
using System.Web.Http.Results;

namespace WebApp
{
    public class UpdateController : ApiController
    {
        public IHttpActionResult Post([FromUri] string id)
        {
            var Authorization = System.Configuration.ConfigurationManager.AppSettings["Authorization"];
            if (Request.Headers.Contains("Authorization") && Request.Headers.GetValues("Authorization").Any(item=>item == Authorization))
            {
                switch (id)
                {
                    case "alerts":
                    case "alerts_test":
                    case "vehiclepositions":
                        {
                            var task = this.Request.Content.ReadAsStreamAsync();
                            task.Wait();
                            Stream requestStream = task.Result;
                            return writeFile(requestStream, id, ".bin");
                        }
                    case "tripupdates":
                        {
                            var task = this.Request.Content.ReadAsStreamAsync();
                            task.Wait();
                            Stream requestStream = task.Result;
                            return writeFile(requestStream, "tripupdates_failover", ".bin");
                        }
                    case "nextbus_current":
                    case "nextbus_new":
                        {
                            var task = this.Request.Content.ReadAsStreamAsync();
                            task.Wait();
                            Stream requestStream = task.Result;
                            return writeFile(requestStream, id, ".xml");
                        }
                    case "current":
                    case "current_swiftly":
                        {
                            var task = this.Request.Content.ReadAsStreamAsync();
                            task.Wait();
                            Stream requestStream = task.Result;
                            return writeFile(requestStream, id, ".zip");
                        }
                    default:
                        return BadRequest();
                }
            }
            else
            {
                return new StatusCodeResult(HttpStatusCode.Forbidden, Request);
            }
        }

        private IHttpActionResult writeFile(Stream requestStream, string file, string extension)
        {
            try
            {
                string filePath = HttpContext.Current.Server.MapPath("~/" + file + extension);
                Stream fileStream = File.Create(filePath);
                MemoryStream ms = new MemoryStream();
                requestStream.CopyTo(fileStream);
                requestStream.CopyTo(ms);
                fileStream.Close();
                requestStream.Close();
                return Created(filePath, ms.ToArray());
            }
            catch (IOException)
            {
                return InternalServerError();
            }
        }
    }
}