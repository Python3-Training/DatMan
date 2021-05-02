/* Manually Updated.

   THIS CLASS WAS GENERATED BY SQLMate .03
   The targeted SQL technology is SQLite3.
   Test case main.java documents tested level of support.
   Your project will need to include sqlite-jdbc.jar:
   -We used sqlite-jdbc-3.8.11.2.jar
 */
package com.soft9000.qna1;

import java.sql.Connection;
import java.sql.PreparedStatement;
import java.sql.ResultSet;
import java.sql.SQLException;
import java.sql.Statement;
import java.util.ArrayList;
import java.util.List;
import java.sql.DriverManager;
import com.soft9000.SQLMate.EColumnType;
import com.soft9000.SQLMate.SqlColumn;

public class QuestDAO {

    public static final int NO_ID = -1;

    public static String CONN_STRING = "jdbc:sqlite:com/soft9000/QuestDAO";

    public static Connection Connect() throws ClassNotFoundException, SQLException {
        return Connect(CONN_STRING);
    }

    public static Connection Connect(String fileName) throws ClassNotFoundException, SQLException {
        if (fileName == null) {
            throw new SQLException("File name cannot be NULL.");
        }

        Class.forName("org.sqlite.JDBC");
        Connection conn = DriverManager.getConnection(fileName);
        return conn;
    }

    public static void Cleanup(Connection conn) throws SQLException {
        if (conn == null) {
            throw new SQLException("Connection Object Reference is NULL.");
        }

        Statement ref = conn.createStatement();
        ref.execute("VACUUM");
    }

    int ID = NO_ID;
    String KID = "";
    String GID = "";
    String Question = "";
    String Answer = "";
    String Difficulty = "";
    String Association = "";
    String Status = "";
    String Language = "";
    int Code1 = 0;
    int Code2 = 0;
    float Version = 0.0f;

    public int getID() {
        return this.ID;
    }

    public String getKID() {
        return this.KID;
    }

    public String getGID() {
        return this.GID;
    }

    public String getQuestion() {
        return this.Question;
    }

    public String getAnswer() {
        return this.Answer;
    }

    public String getDifficulty() {
        return this.Difficulty;
    }

    public String getAssociation() {
        return this.Association;
    }

    public String getStatus() {
        return this.Status;
    }

    public String getLanguage() {
        return this.Language;
    }

    public int getCode1() {
        return this.Code1;
    }

    public int getCode2() {
        return this.Code2;
    }

    public float getVersion() {
        return this.Version;
    }

    public boolean setID(int param) {
        this.ID = param;
        return true;
    }

    public boolean setKID(String param) {
        if (param == null) {
            return false;
        }
        this.KID = param;
        return true;
    }

    public boolean setGID(String param) {
        if (param == null) {
            return false;
        }
        this.GID = param;
        return true;
    }

    public boolean setQuestion(String param) {
        if (param == null) {
            return false;
        }
        this.Question = param;
        return true;
    }

    public boolean setAnswer(String param) {
        if (param == null) {
            return false;
        }
        this.Answer = param;
        return true;
    }

    public boolean setDifficulty(String param) {
        if (param == null) {
            return false;
        }
        this.Difficulty = param;
        return true;
    }

    public boolean setAssociation(String param) {
        if (param == null) {
            return false;
        }
        this.Association = param;
        return true;
    }

    public boolean setStatus(String param) {
        if (param == null) {
            return false;
        }
        this.Status = param;
        return true;
    }

    public boolean setLanguage(String param) {
        if (param == null) {
            return false;
        }
        this.Language = param;
        return true;
    }

    public boolean setCode1(int param) {
        this.Code1 = param;
        return true;
    }

    public boolean setCode2(int param) {
        this.Code2 = param;
        return true;
    }

    public boolean setVersion(float param) {
        this.Version = param;
        return true;
    }

    public boolean insert(Connection conn) throws SQLException {
        if (conn == null) {
            throw new SQLException("Connection Object Reference is NULL.");
        }

        PreparedStatement ref = conn.prepareStatement("INSERT INTO Questions (KID, GID, Question, Answer, Difficulty, Association, Status, Language, Code1, Code2, Version ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?) ;");
        ref.setString(1, this.getKID());
        ref.setString(2, this.getGID());
        ref.setString(3, this.getQuestion());
        ref.setString(4, this.getAnswer());
        ref.setString(5, this.getDifficulty());
        ref.setString(6, this.getAssociation());
        ref.setString(7, this.getStatus());
        ref.setString(8, this.getLanguage());
        ref.setInt(9, this.getCode1());
        ref.setInt(10, this.getCode2());
        ref.setFloat(11, this.getVersion());
        int result = ref.executeUpdate();
        return (result == 1);
    }

    public List<QuestDAO> select(Connection conn, String sqlSelect) throws SQLException {
        if (conn == null) {
            throw new SQLException("Connection Object Reference is NULL.");
        }

        Statement smt = conn.createStatement();
        ResultSet set = smt.executeQuery(sqlSelect);
        ArrayList<QuestDAO> result = new ArrayList<QuestDAO>();
        while (set.next()) {
            QuestDAO ref = new QuestDAO();
            ref.setID(set.getInt("ID"));
            ref.setKID(set.getString("KID"));
            ref.setGID(set.getString("GID"));
            ref.setQuestion(set.getString("Question"));
            ref.setAnswer(set.getString("Answer"));
            ref.setDifficulty(set.getString("Difficulty"));
            ref.setAssociation(set.getString("Association"));
            ref.setStatus(set.getString("Status"));
            ref.setLanguage(set.getString("Language"));
            ref.setCode1(set.getInt("Code1"));
            ref.setCode2(set.getInt("Code2"));
            ref.setVersion(set.getFloat("Version"));
            result.add(ref);
        }

        return result;
    }

    public boolean update(Connection conn) throws SQLException {
        if (conn == null) {
            throw new SQLException("Connection Object Reference is NULL.");
        }

        PreparedStatement ref = conn.prepareStatement("UPDATE Questions SET KID = ?, GID = ?, Question = ?, Answer = ?, Difficulty = ?, Association = ?, Status = ?, Language = ?, Code1 = ?, Code2 = ?, Version = ? WHERE ID = ? ;");
        ref.setString(1, this.getKID());
        ref.setString(2, this.getGID());
        ref.setString(3, this.getQuestion());
        ref.setString(4, this.getAnswer());
        ref.setString(5, this.getDifficulty());
        ref.setString(6, this.getAssociation());
        ref.setString(7, this.getStatus());
        ref.setString(8, this.getLanguage());
        ref.setInt(9, this.getCode1());
        ref.setInt(10, this.getCode2());
        ref.setFloat(11, this.getVersion());
        ref.setInt(12, this.getID());
        int result = ref.executeUpdate();
        return (result == 1);
    }

    public boolean delete(Connection conn) throws SQLException {
        if (conn == null) {
            throw new SQLException("Connection Object Reference is NULL.");
        }

        if (this.getID() == NO_ID) {
            throw new SQLException("Object ID is NULL.");
        }

        Statement ref = conn.createStatement();
        int result = ref.executeUpdate("DELETE FROM Questions WHERE ID = " + this.getID() + " ;");
        return (result == 1);
    }

    public void createTable(Connection conn) throws SQLException {
        if (conn == null) {
            throw new SQLException("Connection Object Reference is NULL.");
        }

        Statement ref = conn.createStatement();
        String sql = "CREATE TABLE IF NOT EXISTS Questions (ID Integer PRIMARY KEY AUTOINCREMENT, KID Text, GID Text, Question Text, Answer Text, Difficulty Text, Association Text, Status Text, Language Text, Code1 Integer, Code2 Integer, Version Real) ;";
        ref.execute(sql);
    }

    public void deleteTable(Connection conn) throws SQLException {
        if (conn == null) {
            throw new SQLException("Connection Object Reference is NULL.");
        }

        Statement ref = conn.createStatement();
        String sql = "DROP TABLE IF EXISTS Questions ;";
        ref.execute(sql);
    }

    public static List<SqlColumn> GetFieldInfo() {
        List<SqlColumn> result = new ArrayList<SqlColumn>();
        result.add(new SqlColumn("ID", EColumnType.Integer));
        result.add(new SqlColumn("KID", EColumnType.Text));
        result.add(new SqlColumn("GID", EColumnType.Text));
        result.add(new SqlColumn("Question", EColumnType.Text));
        result.add(new SqlColumn("Answer", EColumnType.Text));
        result.add(new SqlColumn("Difficulty", EColumnType.Text));
        result.add(new SqlColumn("Association", EColumnType.Text));
        result.add(new SqlColumn("Status", EColumnType.Text));
        result.add(new SqlColumn("Language", EColumnType.Text));
        result.add(new SqlColumn("Code1", EColumnType.Integer));
        result.add(new SqlColumn("Code2", EColumnType.Integer));
        result.add(new SqlColumn("Version", EColumnType.Real));
        return result;
    }

    public static void main(String... args) throws ClassNotFoundException, SQLException {
        Connection conn = Connect("jdbc:sqlite:~test.tmp");
        QuestDAO ref = new QuestDAO();

// TEST TABLE OPS:
        ref.deleteTable(conn);
        ref.createTable(conn);

// TEST INSERT:
        ref.setID(1);
        ref.setKID("data2");
        ref.setGID("data3");
        ref.setQuestion("data4");
        ref.setAnswer("data5");
        ref.setDifficulty("data6");
        ref.setAssociation("data7");
        ref.setStatus("data8");
        ref.setLanguage("data9");
        ref.setCode1(10);
        ref.setCode2(11);
        ref.setVersion(12.12f);
        if (ref.getID() != 1) {
            throw new SQLException("Test Case 'checker 1.1' Error");
        }

        if (ref.getKID().equals("data2") == false) {
            throw new SQLException("Test Case 'checker 1.2' Error");
        }

        if (ref.getGID().equals("data3") == false) {
            throw new SQLException("Test Case 'checker 1.3' Error");
        }

        if (ref.getQuestion().equals("data4") == false) {
            throw new SQLException("Test Case 'checker 1.4' Error");
        }

        if (ref.getAnswer().equals("data5") == false) {
            throw new SQLException("Test Case 'checker 1.5' Error");
        }

        if (ref.getDifficulty().equals("data6") == false) {
            throw new SQLException("Test Case 'checker 1.6' Error");
        }

        if (ref.getAssociation().equals("data7") == false) {
            throw new SQLException("Test Case 'checker 1.7' Error");
        }

        if (ref.getStatus().equals("data8") == false) {
            throw new SQLException("Test Case 'checker 1.8' Error");
        }

        if (ref.getLanguage().equals("data9") == false) {
            throw new SQLException("Test Case 'checker 1.9' Error");
        }

        if (ref.getCode1() != 10) {
            throw new SQLException("Test Case 'checker 1.10' Error");
        }

        if (ref.getCode2() != 11) {
            throw new SQLException("Test Case 'checker 1.11' Error");
        }

        if (ref.getVersion() != 12.12f) {
            throw new SQLException("Test Case 'checker 1.12' Error");
        }

        if (ref.insert(conn) == false) {
            throw new SQLException("Test Case 'insert' Error");
        }

// TEST SELECT:
        List<QuestDAO> zlist;
        zlist = ref.select(conn, "SELECT * FROM Questions ;");
        if (zlist.isEmpty()) {
            throw new SQLException("Test Case 'select 1' Error");
        }

        ref = zlist.get(0);
        if (ref.getKID().equals("data2") == false) {
            throw new SQLException("Test Case 'checker 1.2' Error");
        }

        if (ref.getGID().equals("data3") == false) {
            throw new SQLException("Test Case 'checker 1.3' Error");
        }

        if (ref.getQuestion().equals("data4") == false) {
            throw new SQLException("Test Case 'checker 1.4' Error");
        }

        if (ref.getAnswer().equals("data5") == false) {
            throw new SQLException("Test Case 'checker 1.5' Error");
        }

        if (ref.getDifficulty().equals("data6") == false) {
            throw new SQLException("Test Case 'checker 1.6' Error");
        }

        if (ref.getAssociation().equals("data7") == false) {
            throw new SQLException("Test Case 'checker 1.7' Error");
        }

        if (ref.getStatus().equals("data8") == false) {
            throw new SQLException("Test Case 'checker 1.8' Error");
        }

        if (ref.getLanguage().equals("data9") == false) {
            throw new SQLException("Test Case 'checker 1.9' Error");
        }

        if (ref.getCode1() != 10) {
            throw new SQLException("Test Case 'checker 1.10' Error");
        }

        if (ref.getCode2() != 11) {
            throw new SQLException("Test Case 'checker 1.11' Error");
        }

        if (ref.getVersion() != 12.12f) {
            throw new SQLException("Test Case 'checker 1.12' Error");
        }

// TEST UPDATE:
        ref.setKID("data12");
        ref.setGID("data13");
        ref.setQuestion("data14");
        ref.setAnswer("data15");
        ref.setDifficulty("data16");
        ref.setAssociation("data17");
        ref.setStatus("data18");
        ref.setLanguage("data19");
        ref.setCode1(20);
        ref.setCode2(21);
        ref.setVersion(22.22f);
        if (ref.update(conn) == false) {
            throw new SQLException("Test Case 'update 1' Error");
        }

        if (ref.getKID().equals("data12") == false) {
            throw new SQLException("Test Case 'checker 1.12' Error");
        }

        if (ref.getGID().equals("data13") == false) {
            throw new SQLException("Test Case 'checker 1.13' Error");
        }

        if (ref.getQuestion().equals("data14") == false) {
            throw new SQLException("Test Case 'checker 1.14' Error");
        }

        if (ref.getAnswer().equals("data15") == false) {
            throw new SQLException("Test Case 'checker 1.15' Error");
        }

        if (ref.getDifficulty().equals("data16") == false) {
            throw new SQLException("Test Case 'checker 1.16' Error");
        }

        if (ref.getAssociation().equals("data17") == false) {
            throw new SQLException("Test Case 'checker 1.17' Error");
        }

        if (ref.getStatus().equals("data18") == false) {
            throw new SQLException("Test Case 'checker 1.18' Error");
        }

        if (ref.getLanguage().equals("data19") == false) {
            throw new SQLException("Test Case 'checker 1.19' Error");
        }

        if (ref.getCode1() != 20) {
            throw new SQLException("Test Case 'checker 1.20' Error");
        }

        if (ref.getCode2() != 21) {
            throw new SQLException("Test Case 'checker 1.21' Error");
        }

        if (ref.getVersion() != 22.22f) {
            throw new SQLException("Test Case 'checker 1.22' Error");
        }

// TEST DELETE:
        if (ref.delete(conn) == false) {
            throw new SQLException("Test Case 'delete' Error");
        }

        ref.deleteTable(conn);
    }

    boolean assign(final BasicQuestion obj) {
        if (obj == null) {
            return false;
        }
        this.GID = obj.GID;
        this.KID = obj.KID;
        this.Difficulty = obj.Difficulty;
        this.Answer = obj.Answer;
        this.Question = obj.Question;
        this.Association = obj.Association;
        this.Code1 = 0;
        this.Code2 = 0;
        this.Language = "english";
        this.Status = "undefined";
        this.Version = 0.1F;
        return true;
    }

}
