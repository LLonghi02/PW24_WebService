
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

    @Override
    protected void doGet(HttpServletRequest request, HttpServletResponse response) throws ServletException, IOException {
        PrintWriter out = response.getWriter();
        out.println("doGet chiamato.");
        handleRequest(request, response);
    }

    @Override
    protected void doPost(HttpServletRequest request, HttpServletResponse response) throws ServletException, IOException {
        PrintWriter out = response.getWriter();
        out.println("doPost chiamato.");
        handleRequest(request, response);
    }

    private void handleRequest(HttpServletRequest req, HttpServletResponse resp) throws IOException {
        // Imposta il tipo di contenuto della risposta
        resp.setContentType("text/html");
        PrintWriter out = resp.getWriter();

        // Stampa il metodo della richiesta per il debug
        out.println("<p>Metodo della richiesta: " + req.getMethod() + "</p>");

        // URL del webservice remoto su Altervista
        String remoteUrl = "http://servsanitariopw9.altervista.org/WS.php";

        // Ottieni i dati dal webservice remoto
        out.println("<p>Recupero dati dal webservice remoto...</p>");
        String data = fetchDataFromRemoteService(remoteUrl);
        out.println("<p>Dati recuperati dal webservice remoto: " + data + "</p>");

        // URL del webservice locale Django
        String localUrl = "http://localhost:8000/fetch-and-save/";

        // Invia i dati al webservice locale Django
        out.println("<p>Invio dati al webservice locale Django...</p>");
        sendToDjango(localUrl, data, resp);

        // Risposta al client
        out.println("<p>Dati trasferiti al webservice locale Django con successo.</p>");
        out.flush(); // Assicurati che tutti i dati siano scritti nella risposta
    }

    private String fetchDataFromRemoteService(String urlString) throws IOException {
        // Connessione HTTP per inviare una richiesta POST al webservice remoto
        URL url = new URL(urlString);
        HttpURLConnection conn = (HttpURLConnection) url.openConnection();
        conn.setRequestMethod("POST");
        System.out.println("Richiesta POST inviata a: " + urlString);

        // Leggi la risposta dal webservice remoto
        try (BufferedReader reader = new BufferedReader(new InputStreamReader(conn.getInputStream()))) {
            StringBuilder responseBuilder = new StringBuilder();
            String line;
            while ((line = reader.readLine()) != null) {
                responseBuilder.append(line);
            }
            System.out.println("Risposta dal webservice remoto ricevuta.");
            return responseBuilder.toString();
        }
    }

    private void sendToDjango(String urlString, String data, HttpServletResponse resp) throws IOException {
        PrintWriter out = resp.getWriter();
        
        URL url = new URL(urlString);
        HttpURLConnection conn = (HttpURLConnection) url.openConnection();
        conn.setRequestMethod("POST");
        conn.setRequestProperty("Content-Type", "application/json");
        conn.setDoOutput(true);
        out.println("Richiesta POST inviata a: " + urlString);
        out.println("Dati inviati: " + data);

        // Scrivi i dati nel corpo della richiesta
        try (OutputStream os = conn.getOutputStream()) {
            byte[] input = data.getBytes("utf-8");
            os.write(input, 0, input.length);
            os.flush();
            out.println("Dati inviati al webservice locale Django.");
        } catch (IOException e) {
            System.err.println("Errore durante l'invio dei dati: " + e.getMessage());
            throw e;
        }

        // Leggi la risposta dal webservice locale
        StringBuilder responseBuilder = new StringBuilder();
        try (BufferedReader reader = new BufferedReader(new InputStreamReader(conn.getInputStream(), "utf-8"))) {
            String line;
            while ((line = reader.readLine()) != null) {
                responseBuilder.append(line);
            }
            out.println("Risposta dal webservice locale Django ricevuta: " + responseBuilder.toString());
        } catch (IOException e) {
            System.err.println("Errore durante la lettura della risposta: " + e.getMessage());
            throw e;
        } finally {
            // Chiudi la connessione
            conn.disconnect();
            out.println("Connessione chiusa.");
        }
    }

}
