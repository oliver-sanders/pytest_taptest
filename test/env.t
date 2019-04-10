#!/bin/bash

echo '1..1'

if [[ $FOO == 'foo' ]]; then
    echo 'ok 1 - foo'
else
    echo 'not ok 1 - foo'
fi
