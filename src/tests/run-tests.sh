#!/usr/bin/env bash

# Convenience script providing a higher-level CLI
# for running tests selectively

args_ok=true
test_colour_space=""
test_codec=""
test_file_extension=""
test_cmd="pytest"
test_dir="$GiftGrab_SOURCE_DIR/tests"
test_file_frame_rate=30
test_file_frame_count=15
test_file_frame_width=128
test_file_frame_height=64

function parse_colour()
{
    if [ "$1" = "bgra" ] || [ "$1" = "i420" ] || [ "$1" = "uyvy" ]; then
        test_colour_space=$1
    else
        args_ok=false
    fi
}

function parse_codec()
{
    if [ "$1" = "hevc" ]; then
        test_file_extension="mp4"
    elif [ "$1" = "xvid" ]; then
        test_file_extension="avi"
    elif [ "$1" = "vp9" ]; then
        test_file_extension="webm"
    else
        args_ok=false
    fi

    if [ "$args_ok" = true ]; then
        test_codec=$1
    fi
}

THIS_SCRIPT="$(basename "$(test -L "${BASH_SOURCE[0]}" && readlink "$0" || echo "$0")")"

if [ $# -lt 1 ]; then
    args_ok=false
elif [ "$1" = "encode" ] || [ "$1" = "decode" ];then
    if [ $# -ne "3" ]; then
        args_ok=false
    else
        parse_codec $2
        parse_colour $3
        if [ "$args_ok" = true ]; then
            test_cmd="$test_cmd --colour-space=$test_colour_space"
            if [ "$1" = "encode" ]; then
                test_cmd="$test_cmd --codec=$test_codec $test_dir/target"
            else  # decode
                test_file="$test_dir/files/data"
                test_file="$test_file/video_${test_file_frame_count}frames"
                test_file="${test_file}_${test_file_frame_rate}fps"
                test_file="${test_file}.${test_file_extension}"
                test_cmd="$test_cmd --filepath=$test_file"
                test_cmd="$test_cmd --frame-rate=$test_file_frame_rate"
                test_cmd="$test_cmd --frame-count=$test_file_frame_count"
                test_cmd="$test_cmd --frame-width=$test_file_frame_width"
                test_cmd="$test_cmd --frame-height=$test_file_frame_height"
                test_cmd="$test_cmd $test_dir/files -m observer_pattern"
            fi
        fi
    fi
elif [ "$1" = "numpy" ]; then
    if [ $# -ne "2" ]; then
        args_ok=false
    else
        parse_colour $2
        if [ "$test_colour_space" = "uyvy" ]; then
            args_ok=false
        else
            test_cmd="$test_cmd --colour-space=$test_colour_space"
            test_cmd="$test_cmd $test_dir/videoframe -m numpy_compatibility"
        fi
    fi
elif [ "$1" = "epiphan-dvi2pcieduo" ]; then
    printf "$1 option not implemented yet\n"  # TODO
elif [ "$1" = "network" ]; then
    printf "$1 option not implemented yet\n"  # TODO
elif [ "$1" = "blackmagic-decklinksdi4k" ]; then
    printf "$1 option not implemented yet\n"  # TODO
else
    args_ok=false
fi

if [ "$args_ok" != true ];
then
    printf "Usage:\t${THIS_SCRIPT} encode | decode CODEC COLOUR\n"
    printf "\tCODEC should be one of hevc, xvid, or vp9\n"
    printf " or:\tCOLOUR should be one of bgra, i420, or uyvy\n"
    printf " or:\t${THIS_SCRIPT} numpy bgra | i420\n"
    printf " or:\t${THIS_SCRIPT} epiphan-dvi2pcieduo bgra | i420\n"
    printf " or:\t${THIS_SCRIPT} network\n"
    printf " or:\t${THIS_SCRIPT} blackmagic-decklinksdi4k\n"
    exit 1
fi

echo $test_cmd
