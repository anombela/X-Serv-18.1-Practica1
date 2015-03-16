#!/usr/bin/python

import webapp


class urlApp(webapp.webApp):

    urls1 = {}  # clave: url real y valor el numero
    urls2 = {}  # clave el numero y valor la url real
    urlcorta = 0

    def parse(self, request):

        metodo = request.split(' ', 2)[0]
        recurso = request.split(' ', 2)[1]
        miurl = request.split(' ', 4)[3].split('\n')[0]

        if metodo == 'POST':
            cuerpo = request.split('\r\n\r\n', 1)[1]

        elif metodo == 'GET':
            cuerpo = ''
        return(metodo, recurso, cuerpo, miurl)

    def process(self, resourceName):
        formulario = ('<form action="" method="POST">Escribir url larga:'
                      + '<input type="text" name="nombre" value="" />'
                      + '<input type="submit" value="Acortar" /></form>')

        if resourceName[0] == 'POST':
            cuerpo = resourceName[2].split('=')[1]

            if cuerpo == "":
                return ("404 Not Found", "<html><body>url no introducida" +
                                         "</body></html>")

            if cuerpo.find("http%3A%2F%2F") >= 0:
                cuerpo = cuerpo.split('http%3A%2F%2F')[1]

            cuerpo = "http://" + cuerpo

            if cuerpo in self.urls1:
                urlcorta = self.urls1[cuerpo]
            else:

                urlcorta = self.urlcorta
                self.urlcorta = self.urlcorta + 1
                self.urls1[cuerpo] = urlcorta  # introduce en dos diccionarios
                self.urls2[urlcorta] = cuerpo

            return ("200 OK", "<html><body>URL original: " +
                              "<a href=" + cuerpo + ">" + cuerpo + "</a>" +
                              "</br>URL acortada: " +
                              "<a href=" + str(urlcorta) + ">" +
                              resourceName[3] + "/" + str(urlcorta) + "</a>" +
                              "</p><a href=" + "http://" + resourceName[3] +
                              "> volver </a>""</body></html>")

        elif resourceName[0] == 'GET':
            if resourceName[1] == '/':
                return ("200 OK", "<html><body>" + formulario +
                                  "Urls almacenadas:</br>"+str(self.urls1) +
                                  "</body></html>")
            else:
                try:
                    print resourceName[1]
                    url = self.urls2[int(resourceName[1][1:])]
                    return("300 Redirect", "<html><head><meta http-equiv" +
                                           "='refresh'content='0;url=" +
                                           url + "'></head></html>")
                except KeyError:
                    return("404 Not Found", "<html><body>" + formulario +
                                            "<p>Recurso no encontrado</p>" +
                                            "</body></html>")

                except IndexError:
                    return("404 Not Found", "<html><body>" + formulario + "<p>"
                                            + "Recurso no encontrado</p>" +
                                            "</body></html>")
        else:
            return ("404 Not Found", "<html><body>Metodo desconocido" +
                                     "</body></html>")


if __name__ == "__main__":
    testWebApp = urlApp("localhost", 1235)
