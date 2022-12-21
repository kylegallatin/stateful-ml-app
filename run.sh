#!/bin/bash

NUM_WORKERS=5
FILE="additional_config.txt"

function test_update() {
    update_variable=$1
    update_value=$2
    python test.py --key $update_variable --value $update_value --num-workers $NUM_WORKERS
}

function run_app() {
    python app.py --num-workers $NUM_WORKERS
}

function main() {
    if [ "$#" -eq 0 ]; then 
        if [ -f $FILE ]; then
            rm $FILE
        fi
        echo "Init" > $FILE
        run_app
    else
        action=$1; shift
        case $action in
            test_global_variable)
                test_update "global_data" "new_data"
                ;;
            test_mp_manager)
                test_update "multiprocess_manager" "new_manager_data"
                ;;
            *)
                echo "Wrong option"
                exit 1
                ;;
        esac
    fi
}

program_name=$0
main "$@"