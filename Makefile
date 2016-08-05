CC := g++# Compiler

DEPDIR = .d# Dependency information directory
$(shell mkdir -p $(DEPDIR) >/dev/null)

DEPFLAGS = -MT $@ -MMD -MP -MF $(DEPDIR)/$*.Td

# Compile command includes gcc flags for dependency generation:
COMPILE = $(CC) $(DEPFLAGS) $(CPPFLAGS) -c

# Move temporary generated dependecies to permanent location post-compilation:
POSTCOMPILE = mv -f $(DEPDIR)/$*.Td $(DEPDIR)/$*.d

# List of .cpp and .o files:
CPP_FILES = $(wildcard src/*.cpp) $(wildcard src/*/*.cpp)
OBJ_FILES = $(addprefix obj/, $(notdir $(CPP_FILES:.cpp=.o)))

run: bin/mrpg
	./bin/mrpg

# Executable depends on all .o files:
bin/mrpg: $(OBJ_FILES)
	$(CC) -O2 -Wall -o $@ $(OBJ_FILES)

obj/%.o: src/%.cpp
obj/%.o: src/%.cpp $(DEPDIR)/%.d
	#$(CC) -c -Wall $< -o $@
	$(COMPILE) $(OUTPUT_OPTION) $<
	$(POSTCOMPILE)

obj/%.o: src/*/%.cpp
obj/%.o: src/*/%.cpp $(DEPDIR)/%.d
	#$(CC) -c -Wall $< -o $@
	$(COMPILE) $(OUTPUT_OPTION) $<
	$(POSTCOMPILE)


# Can be used to print variable: "make print-COMPILE"
print-%  : ; @echo $* = $($*)

clean:
	rm -rf bin
	rm -rf obj
	mkdir bin
	mkdir obj

.PHONY: clean run

$(DEPDIR)/%.d: ;
.PRECIOUS: $(DEPDIR)/%.d bin/mrpg

-include $(patsubst %,$(DEPDIR)/%.d,$(basename $(SRCS)))
