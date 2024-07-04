package config

import (
	"database/sql"
	"fmt"
	"log"
	"net/url"
	"os"

	database "patientAuth/db"

	"github.com/joho/godotenv"
	_ "github.com/lib/pq"
)

var dbInstance *sql.DB

func InitializeDB() (*sql.DB, error) {
	if err := godotenv.Load(); err != nil {
		log.Println("Error loading the .env file:", err)
		return nil, err
	}

	connStr := os.Getenv("CONN_STRING")
	secret := os.Getenv("SECRET")

	db, err := setDBConnection(connStr, secret)
	if err != nil {
		return nil, fmt.Errorf("error connecting to database: %v", err)
	}

	dbInstance = db
	return dbInstance, nil
}

func DBRepository() (*database.Queries, error) {
	if dbInstance == nil {
		return nil, fmt.Errorf("database is not initialized")
	}

	dbRepository := database.New(dbInstance)
	return dbRepository, nil
}

func setDBConnection(connStr, password string) (*sql.DB, error) {
	if password == "" {
		return nil, fmt.Errorf("password variable is not defined")
	}

	encodedPassword := url.QueryEscape(password)
	connStr = fmt.Sprintf(connStr, encodedPassword)

	db, err := sql.Open("postgres", connStr)
	if err != nil {
		return nil, fmt.Errorf("error opening database connection: %v", err)
	}

	if err = db.Ping(); err != nil {
		db.Close()
		return nil, fmt.Errorf("error connecting to database: %v", err)
	}

	return db, nil
}
