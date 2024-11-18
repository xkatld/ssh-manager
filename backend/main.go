package main

import (
    "database/sql"
    "log"

    "github.com/gin-gonic/gin"
    _ "github.com/mattn/go-sqlite3"
)

type SSHConnection struct {
    ID       int    `json:"id"`
    Name     string `json:"name"`
    Host     string `json:"host"`
    Port     int    `json:"port"`
    Username string `json:"username"`
    Password string `json:"password"`
    Category string `json:"category"`
}

func initDatabase() *sql.DB {
    db, err := sql.Open("sqlite3", "./ssh_manager.db")
    if err != nil {
        log.Fatal(err)
    }

    _, err = db.Exec(`
        CREATE TABLE IF NOT EXISTS ssh_connections (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT,
            host TEXT,
            port INTEGER,
            username TEXT,
            password TEXT,
            category TEXT
        )
    `)
    if err != nil {
        log.Fatal(err)
    }

    return db
}

func main() {
    db := initDatabase()
    defer db.Close()

    r := gin.Default()
    r.Use(gin.Logger())
    r.Use(gin.Recovery())

    r.POST("/ssh", func(c *gin.Context) {
        var conn SSHConnection
        if err := c.BindJSON(&conn); err != nil {
            c.JSON(400, gin.H{"error": err.Error()})
            return
        }

        result, err := db.Exec(
            "INSERT INTO ssh_connections (name, host, port, username, password, category) VALUES (?, ?, ?, ?, ?, ?)",
            conn.Name, conn.Host, conn.Port, conn.Username, conn.Password, conn.Category,
        )
        if err != nil {
            c.JSON(500, gin.H{"error": err.Error()})
            return
        }

        id, _ := result.LastInsertId()
        conn.ID = int(id)
        c.JSON(200, conn)
    })

    r.GET("/ssh", func(c *gin.Context) {
        rows, err := db.Query("SELECT id, name, host, port, username, category FROM ssh_connections")
        if err != nil {
            c.JSON(500, gin.H{"error": err.Error()})
            return
        }
        defer rows.Close()

        var connections []SSHConnection
        for rows.Next() {
            var conn SSHConnection
            err := rows.Scan(&conn.ID, &conn.Name, &conn.Host, &conn.Port, &conn.Username, &conn.Category)
            if err != nil {
                c.JSON(500, gin.H{"error": err.Error()})
                return
            }
            connections = append(connections, conn)
        }

        c.JSON(200, connections)
    })

    r.Run(":8999")
}
