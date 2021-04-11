/*
 * To change this license header, choose License Headers in Project Properties.
 * To change this template file, choose Tools | Templates
 * and open the template in the editor.
 */
package com.soft9000.qna1;

import java.io.File;
import java.io.FileInputStream;
import java.util.List;
import java.util.logging.Level;
import java.util.logging.Logger;
import javax.json.*;

// Java 1.8: https://repo1.maven.org/maven2/org/glassfish/javax.json/1.0/ (used here!)
// Java 1.9: https://repo1.maven.org/maven2/org/glassfish/javax.json/1.1/
/**
 *
 * @author profnagy
 */
public class JsonOps {

    public static List<BasicQuestion> ImportFile(File file) {
        try {
            FileInputStream fs = new FileInputStream(file);
            JsonReader pzr = Json.createReader(fs);

            JsonArray rows = pzr.readArray();
            for (JsonValue row : rows) {
                System.out.println(row.toString());
            }
            pzr.close();
            fs.close();

        } catch (Exception ex) {
            Logger.getLogger(JsonOps.class.getName()).log(Level.SEVERE, null, ex);
        }
        return null;
    }

    public static void main(String[] args) {
        JsonOps.ImportFile(new File("/d_drive/a5/2020_01_03_TEC/2021_01_01_Python_Related/9000_Python_QnA_2020_12_29/2021_01_01_9000_Python_QnA/ascii.json"));
    }

}
