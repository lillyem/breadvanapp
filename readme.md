# Bread Van App

The **Bread Van App** is a simple Flask MVC project that manages **Drivers** and **Residents**.  
Drivers can be created, scheduled for routes, and have their status/location updated.  
Residents can be created, send stop requests, view their inbox, and track drivers.  

This app uses a **CLI interface** for testing and simulating driver–resident interactions.

---

## Setup Instructions

1. Clone the repository and install dependencies:

   git clone <your-repo-url>
   cd breadvanapp
   pip install -r requirements.txt

2. Initialize the database:

    flask init

3. Run the CLI commands below to test.

## User Commands

| Title    | Command                    |
|------|--------------------------|
| Create User | flask user create "username" "password" |
| List Users | flask user list string |
| List Users (JSON) | flask user list json |

## Test Commands

| Title    | Command                    |
|------|--------------------------|
| Run All Tests | flask test user all |
| Run Unit Tests | flask test user unit |
| Run Integration Tests | flask test user int |

## Driver Commands

| Title    | Command                    |
|------|--------------------------|
| Create Driver | flask driver create "DriverName" "LocationName" |
| Schedule Drive | flask driver schedule "DriverName" "LocationName" ResidentID |
| Check Status | flask driver status "DriverName" |
| Update Location | flask driver update-location "DriverName" "LocationName" |
| Update Status | flask driver update-status "DriverName" "Status" |

## Resident Commands

| Title    | Command                    |
|------|--------------------------|
| Create Resident | flask resident create "ResidentName" "LocationName" |
| Inbox | flask resident inbox "ResidentName" |
| Request Stop | flask resident request-stop "ResidentName" "DriverName" |
| Track Driver | flask resident track "ResidentName" "DriverName" |

## Example Workflow

flask driver create "Alice" "Downtown"  
flask resident create "Bob" "Uptown"  
flask driver schedule "Alice" "Uptown" 1  
flask resident inbox "Bob"  
flask resident request-stop "Bob" "Alice"  
flask resident track "Bob" "Alice"  


