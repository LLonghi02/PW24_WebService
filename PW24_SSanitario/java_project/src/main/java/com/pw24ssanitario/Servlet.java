package com.pw24ssanitario;

import java.io.BufferedReader;
import java.io.IOException;
import java.io.InputStreamReader;
import java.io.OutputStream;
import java.net.HttpURLConnection;
import java.net.URL;

import javax.servlet.ServletException;
import javax.servlet.http.HttpServlet;
import javax.servlet.http.HttpServletRequest;
import javax.servlet.http.HttpServletResponse;

public class Servlet extends HttpServlet {
    
    protected void doGet(HttpServletRequest request, HttpServletResponse response) throws ServletException, IOException {
        // URL del webservice remoto su Altervista
        String remoteUrl = "http://servsanitariopw9.altervista.org/WS.php";
        
        // Connessione HTTP per inviare una richiesta GET al webservice remoto
        URL url = new URL(remoteUrl);
        HttpURLConnection conn = (HttpURLConnection) url.openConnection();
        conn.setRequestMethod("GET");
        
        // Leggi la risposta dal webservice remoto
        BufferedReader reader = new BufferedReader(new InputStreamReader(conn.getInputStream()));
        StringBuilder responseBuilder = new StringBuilder();
        String line;
        while ((line = reader.readLine()) != null) {
            responseBuilder.append(line);
        }
        reader.close();
        
        // Dati ottenuti dal webservice remoto
        String responseData = responseBuilder.toString();
        
        // Ora, possiamo inviare questi dati al webservice locale Django
        sendToDjango(responseData);
        
        // Ritorna una risposta al client (opzionale)
        response.getWriter().write("Dati inviati al webservice locale Django con successo.");
    }
    
    private void sendToDjango(String data) throws IOException {
        // URL del webservice locale Django
        String localUrl = "http://localhost:8000/importer/receive-data/";  // Esempio di URL del webservice locale
        
        // Connessione HTTP per inviare una richiesta POST al webservice locale
        URL url = new URL(localUrl);
        HttpURLConnection conn = (HttpURLConnection) url.openConnection();
        conn.setRequestMethod("POST");
        conn.setRequestProperty("Content-Type", "application/json");
        conn.setDoOutput(true);
        
        // Scrivi i dati da inviare nel corpo della richiesta
        OutputStream os = conn.getOutputStream();
        byte[] input = data.getBytes("utf-8");
        os.write(input, 0, input.length);
        os.flush();
        os.close();
        
        // Leggi la risposta dal webservice locale (opzionale)
        BufferedReader reader = new BufferedReader(new InputStreamReader(conn.getInputStream()));
        StringBuilder responseBuilder = new StringBuilder();
        String line;
        while ((line = reader.readLine()) != null) {
            responseBuilder.append(line);
        }
        reader.close();
        
        // Stampa la risposta dal webservice locale (opzionale)
        System.out.println(responseBuilder.toString());
        
        // Chiudi la connessione
        conn.disconnect();
    }
}
