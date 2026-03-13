 workspace "Microservices Project"  {

    !identifiers hierarchical

    model {
        archetypes {
            user = person {
                tag "User"
            }
            service = container {
                technology "Python"
                tag "Service"
            }
            database = container {
                technology "PostgreSQL"
                tag "Database"
            }
            cache = container {
                technology "Valkey"
                tag "Cache"
            }
            apigateway = container {
                technology "FastAPI"
                tag "API Gateway"
            }
            bot = container {
                technology "Node.js"
                tag "Bot"
            }
            externalservice = softwaresystem {
                tag "External Service"
            }
        }


        u = user "User"
        na = externalservice "nba_api"
        da = externalservice "Discord Platform"

        ss = softwaresystem "NBA Discord Bot System" {
            dsb = bot "Discord Bot"
            api = apigateway "API Gateway"
            ns = service "NBA Service"
            us = service "User Service"
            db = database "Database"
            c = cache "Cache"
        }

        u -> ss "Uses via Discord"
        da -> ss.dsb "Sends events to"
        ss.dsb -> ss.api "Sends requests to"
        ss.api -> ss.ns "HTTPS/API"
        ss.api -> ss.us "HTTPS/API"
        ss.ns -> ss.c "Cached to"
        ss.us -> ss.db "Saved to and read from"
        ss.c -> na "Read from"
    }
    
    views {
        systemcontext ss "Diagram1" {
            include *
            autolayout lr
        }
        container ss "Diagram2" {
            include *
            autolayout lr
        }
        styles {
            element "Element" {
                shape roundedBox
            }
            element "User" {
                shape person
            }
            element "Bot" {
                shape robot
            }
            element "Database" {
                shape cylinder
            }
        }
    }
} 
