if [ -z $1 ]; then
  # Unset arg, just run it normally
  python3 main.py
else
  # Set arg, run it on the core
  taskset -c $1 python3 main.py
fi

