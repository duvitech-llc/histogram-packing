# Makefile for building the histogram packing main application

# Compiler to use (for a PC build using gcc; adjust for STM32H7 cross-compilation)
CC = gcc

# Compiler flags: enable warnings and optimization; adjust the standard as needed.
CFLAGS = -Wall -Wextra -O2 -std=c99

# Target executable name
TARGET = histpack

# Source files (add additional sources if needed)
SRCS = main.c

# Object files (automatically generated from source files)
OBJS = $(SRCS:.c=.o)

# Default rule
all: $(TARGET)

# Link object files to create the target executable
$(TARGET): $(OBJS)
	$(CC) $(CFLAGS) -o $(TARGET) $(OBJS)

# Compile .c files to .o object files
%.o: %.c
	$(CC) $(CFLAGS) -c $< -o $@

# Clean up generated files
clean:
	rm -f $(OBJS) $(TARGET)
