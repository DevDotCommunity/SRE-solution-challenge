# System Health Check Script Solution

This bash script provides a comprehensive system monitoring solution with a user-friendly menu interface. Let's break down each component:

## Script Structure

### 1. Menu Display Function
```bash
display_menu() {
    echo "** System Health Check Script **"
    echo "1. Check Disk Usage"
    echo "2. Monitor Running Services"
    echo "3. Assess Memory Usage"
    echo "4. Evaluate CPU Usage"
    echo "5. Send System Health Report (Automated - Every 4 hours)"
    echo "0. Exit"
    echo -n "Enter your choice: "
}
```
This function creates an interactive menu using simple echo commands. The `-n` flag in the final echo prevents a newline, keeping the cursor on the same line for user input.

### 2. Disk Usage Function
```bash
check_disk_usage() {
    echo "** Disk Usage **"
    df -h
    echo
    # Add logic to analyze disk usage (e.g., warn if above 80%)
}
```
- -Uses df (disk free) command
- -h flag makes output human-readable
- Shows filesystem usage including mounted drives

### 3. Service Monitoring Function
```bash
monitor_services() {
    echo "** Running Services **"
    service --status-all 2>&1 | grep -vE "(dead|not-active)" | grep "+"
    echo
    # Add logic to analyze service status (e.g., identify failed services)
}
```
- `service --status-all` lists all system services
- `grep -vE "(dead|not-active)"` filters out inactive services
- `grep "+"` shows only running services

4. Memory Usage Function
```bash
assess_memory_usage() {
    echo "** Memory Usage **"
    free -h | grep Mem | awk '{print $3 " / " $2 " (" $3/$2*100 "%)"}'
    echo
    # Add logic to analyze memory usage (e.g., warn if above 80%)
}
```
- `free -h` displays memory usage in human-readable format
- `awk` command calculates percentage of used memory
- Shows used/total memory with percentage

### 5. CPU Usage Function
```bash
evaluate_cpu_usage() {
    echo "** CPU Usage **"
    mpstat 1 1 | awk '/Average/ {print 100 - $12 "%"}'
    echo
    # Add logic to analyze CPU usage (e.g., warn if consistently above 80%)
}
```
- Uses mpstat to gather CPU statistics
- Takes 1 sample over 1 second
- Calculates CPU usage percentage

### 6. Email Report Function
```bash
send_report() {
    API_KEY="YOUR_API_KEY"
    RECIPIENT="email@example.com"
    SENDER="email@example.com"
    SUBJECT="System Health Report"

    DISK_USAGE=$(check_disk_usage | paste -sd "<br>" -)
    SERVICES=$(monitor_services | paste -sd "<br>" -)
    MEMORY_USAGE=$(assess_memory_usage | paste -sd "<br>" -)
    CPU_USAGE=$(evaluate_cpu_usage | paste -sd "<br>" -)

    CONTENT="<h1>System Health Report</h1>
             <p><strong>Disk Usage:</strong><br>$DISK_USAGE</p>
             <p><strong>Running Services:</strong><br><pre>$SERVICES</pre></p>
             <p><strong>Memory Usage:</strong><br>$MEMORY_USAGE</p>
             <p><strong>CPU Usage:</strong><br>$CPU_USAGE</p>"

    curl -X POST 'https://api.elasticemail.com/v4/emails' \
         -H "Content-Type: application/json" \
         -H "X-ElasticEmail-ApiKey: $API_KEY" \
         -d "{
      \"Recipients\": [
        {
          \"Email\": \"$RECIPIENT\"
        }
      ],
      \"Content\": {
        \"Body\": [
          {
            \"ContentType\": \"HTML\",
            \"Content\": \"$CONTENT\"
          }
        ],
        \"Subject\": \"$SUBJECT\",
        \"From\": \"$SENDER\"
      }
    }"
}
```
- Uses Elastic Email API for sending reports
- Combines all health checks into HTML format
- Sends formatted email using curl

### 7. Main Program Loop
```bash
if [ -z "$1" ]; then
  # Interactive mode
  while true; do
    clear
    display_menu

    read choice

    case $choice in
      1)
        check_disk_usage
        ;;
      2)
        monitor_services
        ;;
      3)
        assess_memory_usage
        ;;
      4)
        evaluate_cpu_usage
        ;;
      5)
        send_report
        ;;
      0)
        echo "Exiting..."
        exit 0
        ;;
      *)
        echo "Invalid choice. Please try again."
        ;;
    esac
    echo -n "Press any key to continue..."
    read -r -s -n 1
  done
else
  # Non-interactive mode (for cron job)
  send_report
fi
done
```

- Checks if the script is run interactively or by a cron job
- Infinite loop with while true
- clear command keeps interface clean
- case statement handles menu options
- Waits for keypress between operations
### Usage
- Save the script with .sh extension
- Make it executable: chmod +x script.sh
- Run it: ./script.sh
### Key Features
- Menu-driven interface
- Human-readable output
- Error handling
- Automated email reporting
- Clear screen management
- Easy to extend with additional checks


### putting everthing all together 
```bash
#!/bin/bash

# Function to display the menu
display_menu() {
  echo "** System Health Check Script **"
  echo "1. Check Disk Usage"
  echo "2. Monitor Running Services"
  echo "3. Assess Memory Usage"
  echo "4. Evaluate CPU Usage"
  echo "5. Send System Health Report (Automated - Every 4 hours)"
  echo "0. Exit"
  echo -n "Enter your choice: "
}

# Function to check disk usage
check_disk_usage() {
  echo "** Disk Usage **"
  df -h 
  echo
  # Add logic to analyze disk usage (e.g., warn if above 80%)
}

# Function to monitor running services
monitor_services() {
  echo "** Running Services **"
  service --status-all 2>&1 | grep -vE "(dead|not-active)" | grep "+"
  echo
  # Add logic to analyze service status (e.g., identify failed services)
}

# Function to assess memory usage
assess_memory_usage() {
  echo "** Memory Usage **"
  free -h | grep Mem | awk '{print $3 " / " $2 " (" $3/$2*100 "%)"}'
  echo
  # Add logic to analyze memory usage (e.g., warn if above 80%)
}

# Function to evaluate CPU usage
evaluate_cpu_usage() {
  echo "** CPU Usage **"
  mpstat 1 1 | awk '/Average/ {print 100 - $12 "%"}'
  echo
  # Add logic to analyze CPU usage (e.g., warn if consistently above 80%)
}

# Function to send system health report
send_report() {
  API_KEY="YOUR_API_KEY"
  RECIPIENT="recipient@example.com"
  SENDER="sender@example.com"
  SUBJECT="System Health Report"

  DISK_USAGE=$(check_disk_usage | paste -sd "<br>" -)
  SERVICES=$(monitor_services | paste -sd "<br>" -)
  MEMORY_USAGE=$(assess_memory_usage | paste -sd "<br>" -)
  CPU_USAGE=$(evaluate_cpu_usage | paste -sd "<br>" -)

  CONTENT="<h1>System Health Report</h1>
           <p><strong>Disk Usage:</strong><br>$DISK_USAGE</p>
           <p><strong>Running Services:</strong><br><pre>$SERVICES</pre></p>
           <p><strong>Memory Usage:</strong><br>$MEMORY_USAGE</p>
           <p><strong>CPU Usage:</strong><br>$CPU_USAGE</p>"

  curl -X POST 'https://api.elasticemail.com/v4/emails' \
       -H "Content-Type: application/json" \
       -H "X-ElasticEmail-ApiKey: $API_KEY" \
       -d "{
    \"Recipients\": [
      {
        \"Email\": \"$RECIPIENT\"
      }
    ],
    \"Content\": {
      \"Body\": [
        {
          \"ContentType\": \"HTML\",
          \"Content\": \"$CONTENT\"
        }
      ],
      \"Subject\": \"$SUBJECT\",
      \"From\": \"$SENDER\"
    }
  }"
}

# Main loop for user interaction
if [ -z "$1" ]; then
  # Interactive mode
  while true; do
    clear
    display_menu

    read choice

    case $choice in
      1)
        check_disk_usage
        ;;
      2)
        monitor_services
        ;;
      3)
        assess_memory_usage
        ;;
      4)
        evaluate_cpu_usage
        ;;
      5)
        send_report
        ;;
      0)
        echo "Exiting..."
        exit 0
        ;;
      *)
        echo "Invalid choice. Please try again."
        ;;
    esac
    echo -n "Press any key to continue..."
    read -r -s -n 1
  done
else
  # Non-interactive mode (for cron job)
  send_report
fi
```