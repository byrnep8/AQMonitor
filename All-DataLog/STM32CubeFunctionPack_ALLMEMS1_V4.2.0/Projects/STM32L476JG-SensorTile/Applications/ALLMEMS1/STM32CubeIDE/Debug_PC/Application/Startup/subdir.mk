################################################################################
# Automatically-generated file. Do not edit!
# Toolchain: GNU Tools for STM32 (10.3-2021.10)
################################################################################

# Add inputs and outputs from these tool invocations to the build variables 
S_SRCS += \
../Application/Startup/startup_stm32l476xx.s 

S_DEPS += \
./Application/Startup/startup_stm32l476xx.d 

OBJS += \
./Application/Startup/startup_stm32l476xx.o 


# Each subdirectory must supply rules for building sources it contributes
Application/Startup/%.o: ../Application/Startup/%.s Application/Startup/subdir.mk
	arm-none-eabi-gcc -mcpu=cortex-m4 -g3 -c -I"C:/Users/Patrick/STM32CubeIDE/workspace_all_data/i2c_prototype/Core/i2c_adxl345" -I"C:/Users/Patrick/Documents/DCU/Masters Project/All-DataLog/STM32CubeFunctionPack_ALLMEMS1_V4.2.0/Projects/STM32L476JG-SensorTile/Applications/ALLMEMS1/Inc" -I"C:/Users/Patrick/Documents/DCU/Masters Project/ds3231" -I"C:/Users/Patrick/STM32CubeIDE/workspace_all_data/i2c_prototype/Core/Src/SPS30_Git" -I"C:/Users/PByrne/Documents/GitHub/masters_project/i2c_prototype/Core/Src/SPS30_Git" -I"C:/Users/Patrick/Documents/DCU/Masters Project/masters_project/MICS4514_Git" -x assembler-with-cpp -MMD -MP -MF"$(@:%.o=%.d)" -MT"$@" --specs=nano.specs -mfpu=fpv4-sp-d16 -mfloat-abi=softfp -mthumb -o "$@" "$<"

clean: clean-Application-2f-Startup

clean-Application-2f-Startup:
	-$(RM) ./Application/Startup/startup_stm32l476xx.d ./Application/Startup/startup_stm32l476xx.o

.PHONY: clean-Application-2f-Startup

