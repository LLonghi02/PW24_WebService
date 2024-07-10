package com.example.servlet;

import java.io.BufferedReader;
import java.io.InputStreamReader;
import java.io.OutputStream;
import java.io.IOException;
import java.net.HttpURLConnection;
import java.net.URL;
import javax.servlet.ServletException;
import javax.servlet.annotation.WebServlet;
import javax.servlet.http.HttpServlet;
import javax.servlet.http.HttpServletRequest;
import javax.servlet.http.HttpServletResponse;
import org.json.JSONObject;

@WebServlet("/import-data")
public class WebServletImportData extends HttpServlet {
    private static final long serialVersionUID = 1L;
    private static final String REMOTE_URL = "URL_DEL_TUO_WEBSERVICE_REMOTO";
    private static final String LOCAL_URL = "http://localhost:8000/migrazione-dati/";

    @Override
    protected void doGet(HttpServletRequest req, HttpServletResponse resp) throws ServletException, IOException {
        try {
            URL url = new URL(REMOTE_URL);
            HttpURLConnection conn = (HttpURLConnection) url.openConnection();
            conn.setRequestMethod("GET");
            conn.setRequestProperty("Accept", "application/json");

            if (conn.getResponseCode() != 200) {
                throw new RuntimeException("Failed : HTTP error code : " + conn.getResponseCode());
            }

            BufferedReader br = new BufferedReader(new InputStreamReader((conn.getInputStream())));
            String output;
            StringBuilder response = new StringBuilder();

            while ((output = br.readLine()) != null) {
                response.append(output);
            }

            conn.disconnect();

            JSONObject jsonResponse = new JSONObject(response.toString());
            sendToLocalWebService(jsonResponse);

            resp.getWriter().write("Dati migrati con successo!");

        } catch (Exception e) {
            e.printStackTrace();
            resp.getWriter().write("Errore nella migrazione dei dati: " + e.getMessage());
        }
    }

    private void sendToLocalWebService(JSONObject data) throws Exception {
        URL url = new URL(LOCAL_URL);
        HttpURLConnection conn = (HttpURLConnection) url.openConnection();
        conn.setDoOutput(true);
        conn.setRequestMethod("POST");
        conn.setRequestProperty("Content-Type", "application/json");

        OutputStream os = conn.getOutputStream();
        os.write(data.toString().getBytes());
        os.flush();

        if (conn.getResponseCode() != HttpURLConnection.HTTP_OK) {
            throw new RuntimeException("Failed : HTTP error code : " + conn.getResponseCode());
        }

        BufferedReader br = new BufferedReader(new InputStreamReader((conn.getInputStream())));
        String output;
        while ((output = br.readLine()) != null) {
            System.out.println(output);
        }

        conn.disconnect();
    }
}
