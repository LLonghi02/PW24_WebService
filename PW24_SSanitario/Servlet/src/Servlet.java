import java.io.BufferedReader;
import java.io.IOException;
import java.io.InputStreamReader;
import java.io.OutputStream;
import java.net.HttpURLConnection;
import java.net.URL;
import jakarta.servlet.ServletException;
import jakarta.servlet.http.HttpServlet;
import jakarta.servlet.http.HttpServletRequest;
import jakarta.servlet.http.HttpServletResponse;
import java.io.PrintWriter;

public class Servlet extends HttpServlet {

    //Metodo per effettuare richieste Http che utilizzano il metodo GET
    @Override
    protected void doGet(HttpServletRequest request, HttpServletResponse response) throws ServletException, IOException {
        handleRequest(request, response); //Chiamata del metodo per gestire la richiesta
    }

    //Metodo per effettuare richieste Http che utilizzano il metodo GET
    @Override
    protected void doPost(HttpServletRequest request, HttpServletResponse response) throws ServletException, IOException {
        handleRequest(request, response); //Chiamata del metodo per gestire la richiesta
    }

    //Metodo per gestire le richieste effettuate
    private void handleRequest(HttpServletRequest req, HttpServletResponse resp) throws IOException {
        // Imposta il tipo di contenuto della risposta
        resp.setContentType("text/html");

        PrintWriter out = resp.getWriter(); //Oggetto necessario per stampare messaggi sul server Tomcat

        //Generazione di codice html per la definizione di una pagina per l'utente che mostra il risultato dell'esecuzione della servlet
        out.println("<html>");
        out.println("<head>");
        out.println("<title>Risultati della Servlet</title>");
        out.println("<style>");
        out.println("body { font-family: Arial, sans-serif; margin: 20px; padding: 20px; background-color: #955F40; }");
        out.println("h1 { color: #955F40; }");
        out.println("p { font-size: 16px; color: #955F40; }");
        out.println(".container { max-width: 800px; margin: auto; padding: 20px; background: #EBC7A1; border-radius: 8px; box-shadow: 0 0 10px rgba(0,0,0,0.1); }");
        out.println(".status { font-weight: bold; color: #955F40; }");
        out.println(".error { color: #d9534f; }");
        out.println("</style>");
        out.println("</head>");
        out.println("<body>");
        out.println("<div class='container'>");

        out.println("<h1>Risultati della Servlet</h1>");

        //URL del webservice remoto su Altervista
        String remoteUrl = "http://servsanitariopw9.altervista.org/WS.php";

        //Ottenimento dei dati dal webservice remoto
        out.println("<p>Recupero dati dal webservice remoto...</p>");
        String data;
        try {
            data = fetchDataFromRemoteService(remoteUrl); //Chiamata del metodo per il fetch dei dati dal web service remoto (su altervista)
            out.println("<p>Dati recuperati dal webservice remoto.</p>");
        } catch (IOException e) { //Generazione di un'eccezione nel caso si verifichino problemi durante il recupero dei dati
            out.println("<p class='error'>Errore durante il recupero dei dati dal webservice remoto: " + e.getMessage() + "</p>");
            data = "";
        }

        //URL del webservice locale Django
        String localUrl = "http://localhost:8000/fetch-and-save/";

        //Invio i dati al webservice locale Django
        out.println("<p>Invio dati al webservice locale Django...</p>");
        try {
            sendToDjango(localUrl, data, resp); //Chiamata al metodo per l'invio dei dati al web service locale (Django)
            out.println("<p class='status'>Dati trasferiti al webservice locale Django con successo.</p>");
        } catch (IOException e) { //Generazione di un'eccezione nel caso si verifichino problemi durante il l'invio dei dati
            out.println("<p class='error'>Errore durante l'invio dei dati al webservice locale Django: " + e.getMessage() + "</p>");
        }

        out.println("</div>");
        out.println("</body>");
        out.println("</html>");

        out.flush(); //Scrittura di tutti i dati nella risposta
    }

    //Metodo per il recupero dei dati dal web service remoto su altervista
    private String fetchDataFromRemoteService(String urlString) throws IOException {
        //Connessione Http per inviare una richiesta POST al webservice remoto
        URL url = new URL(urlString);
        HttpURLConnection conn = (HttpURLConnection) url.openConnection();
        conn.setRequestMethod("POST");

        //Lettura della risposta dal webservice remoto
        try (BufferedReader reader = new BufferedReader(new InputStreamReader(conn.getInputStream()))) {
            StringBuilder responseBuilder = new StringBuilder();
            String line;
            while ((line = reader.readLine()) != null) {
                responseBuilder.append(line);
            }
            return responseBuilder.toString();
        }
    }

    //Metodo per l'invio dei dati al web service locale Django
    private void sendToDjango(String urlString, String data, HttpServletResponse resp) throws IOException {
        //Connessione Http per inviare una richiesta POST al webservice locale
        URL url = new URL(urlString);
        HttpURLConnection conn = (HttpURLConnection) url.openConnection();
        conn.setRequestMethod("POST");
        conn.setRequestProperty("Content-Type", "application/json"); //Invio di dati in formato json nel corpo della richiesta
        conn.setDoOutput(true);

        //Scrittura dei dati nel corpo della richiesta
        try (OutputStream os = conn.getOutputStream()) {
            byte[] input = data.getBytes("utf-8");
            os.write(input, 0, input.length);
            os.flush();
        } catch (IOException e) { //Generazione di un'eccezione nel caso di errori durante l'invio
            System.err.println("Errore durante l'invio dei dati: " + e.getMessage());
            throw e;
        }

        //Lettura della risposta dal webservice locale
        StringBuilder responseBuilder = new StringBuilder();
        try (BufferedReader reader = new BufferedReader(new InputStreamReader(conn.getInputStream(), "utf-8"))) {
            String line;
            while ((line = reader.readLine()) != null) {
                responseBuilder.append(line);
            }
        } catch (IOException e) {
            System.err.println("Errore durante la lettura della risposta: " + e.getMessage());
            throw e;
        } finally {
            //Chiusura della connessione
            conn.disconnect();
        }
    }
}
