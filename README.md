# Experiment Description

For the main evaluation we built all benchmarks of the suite using the code provided in the HPCC FPGA repository in the [inital version](https://github.com/pc2/HPCC_FPGA/tree/1d8dead9d00a359e0116f0fd2c56206dcbf10d05).
Therefore, we used CMake together with the configuration options specified in the paper to configure the kernel code for each tested board.
Note, that it might be necessary to modify additional build parameters for some of the boards, which are:

- PAC D5005: add -DUSE_SVM=Yes to build the host code with SVM support.
- U280: modify the link settings file path to match the link configuration for HBM or DDR. Disable the link setting generation in case of DDR.

We executed the benchmarks with the data sizes given in the paper and repeated the measurement at least 10 times using the -n option provided by each benchmark.
The best result of these repetitions is automatically reported by the application.
For the host code of the STREAM kernel the runtime parameter `--single-kernel` has to be used for execution to specify the type of the used kernel.

Within the evaluation repository we also provide the benchmark outputs for all experiments and the synthesis reports produced by the OpenCL frameworks.
They are sorted by the used FPGA board and benchmark and can help to reproduce the reported results, if some information might be missing in this explanation.

The additional experiments are executed with modified versions of the code provided in the HPCC FPGA repository.
The modifications are provided in git patches located in the evaluation repository for this paper.
For the investigation with the PAC board, we applied the patch `pac_cba_modifications.patch` to change the order of array initializations.
With the patch `pac_abdc_modification.patch` an additional array is added.

For the OpenCL profiling of the U280 kernels we applied the modifications given in `profiling_modifications.patch`.
The compiled host code will create an additional CSV file located in the execution folder named `detailed_stream_timings.csv`.
It contains the kernel runtimes for each operation and for every kernel replication.
This data was used to investigate the performance issues on the U280 board as documented in the paper.
For the execution of the host code we set the environment variable OMP_NUM_THREADS=1 to force scheduling of the kernels in a defined order 0,1,2,3,... .
We then compiled the host code again with the same patch and the additional build parameter -DREORDER_KERNELS=Yes.
The resulting host code will schedule the kernels in the order 0,16,1,17,2,... where the number represents the memory bank the kernel is linked to.
Also here, OMP_NUM_THREADS is set to 1 for the execution.
The CSV files with the data used in the paper are also provided in the evaluation repository.

The modified copy kernel that was used in the paper to show the possibility to achieve higher bandwidths is given in the patch file `copy_modification.patch`.
The modifications add an additional kernel to the STREAM benchmark: stream_kernel_multi.
The configuration options for the Xilinx compile and link settings files are changed to the ones provided in the patch.
Link settings generation is turned off.
For the experiment we synthesized the kernel using the new target stream_kernel_multi and we build the host code from the patched sources.
We executed the benchmark with the `stream_kernels_multi.xclbin`.
The validation of the execution fails, since we are only using the copy operation in this experiment.
The host code prints the times and performance for all STREAM operations, where only the values for copy are correct.

In another experiment in the paper we reduced the number of used replications for RandomAccess and STREAM to show higher performance.
This was done based on the unmodified HPCC FPGA code.
The host option -r was used in both cases to specify the number of used kernels at runtime, so we ran i.e. ./STREAM_FPGA_xilinx -f ... -r 30 .

To produce the STREAM kernel with a low frequency of 280MHz we also used the unmodified benchmark code.
We used the same configuration options that are given for STREAM in the paper and only increased the buffer size by increasing DEVICE_BUFFER_SIZE to 2^14.

## Evaluation Updates

#### Resolve U280 performance issue

The reason for the performance drop was, that the used schedulers ERT or KDS seem to support just 16 running jobs.
The issue can be resolved by disabling the ERT and KDS scheduler when executing the benchmarks.
This will lead to a fallback to the legacy scheduler.
This can be by creating a file named `xrt.ini` with the following content in the execution directory:

    [Runtime]
    ert=false
    kds=false

More information on that can be found in the [XRT documentation](https://github.com/Xilinx/XRT/blob/master/src/runtime_src/doc/toc/debug-faq.rst#xrt-scheduling-options).
Disabling the scheduler resolved the issue for STREAM and RandomAccess.
The new measurement results can be found in the execution artifacts of each benchmark in the folder `ERT_scheduler_disabled`.
The same bitstreams were used for this experiment, so the synthesis report stay the same.

#### Power Measurements

The power measurements where done for the STREAM benchmark on all four devices.
The benchmark output, the raw measured data in CSV format, and the measurement script are given for each device in the folder `STREAM/power_measurements`.
Stream was executed the same way as in the default run, but the number of repetitions was increased to 100 with the flag `-n 100`.
For the power measurements, the benchmark was executed with the wrapper bash script that is also contained in the same folder.

    ./u280.xbutildump.sh ./STREAM_FPGA_xilinx -f ...

The raw data in the CSV files was used to calculate the average power in Watts.
The STREAM benchmark on CPU was compiled with the Makefile located in `STREAM CPU`.
Power measurement where done during execution using turbostat.
