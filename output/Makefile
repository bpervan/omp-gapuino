# User Test
#------------------------------------------
#TEST_C          = ./omp_trap2a_gap_gap.c

#TEST_C          = ./omp_hello_gap.c
#TEST_C          = ./hello_for_gap.c
TEST_C          = ./omp_pi_gap.c
# For RTOS Jenkins test, it will never finished so add a jenkins test Flag to exit().
MBED_FLAGS     +=-DJENKINS_TEST_FLAG=1

include $(GAP_SDK_HOME)/tools/rules/mbed_rules.mk
