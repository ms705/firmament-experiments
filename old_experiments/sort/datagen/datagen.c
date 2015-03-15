
#include <stdio.h>
#include <stdlib.h>
#include <time.h>

#include <camio/camio.h>

static camio_ostream_t* out      = NULL;
static camio_perf_t* perf_mon    = NULL;

struct camio_datagen_options_t {
  char* clock;
  char* output;
  uint64_t num_records;
  uint64_t record_size;
  uint8_t verbose;
} options ;

void configure_options(int argc, char** argv) {
  camio_options_short_description("datagen");
  camio_options_add(CAMIO_OPTION_OPTIONAL, 'c', "clock",     "Clock description eg tistream", CAMIO_STRING, &options.clock, "tistream" );
  camio_options_add(CAMIO_OPTION_OPTIONAL, 'o', "output", "Output descriptions in camio format. eg log:/file.txt", CAMIO_STRING, &options.output, "std-log");
  camio_options_add(CAMIO_OPTION_OPTIONAL, 'n', "num-records", "Total number of records to generatey.", CAMIO_UINT64, &options.num_records, 1000000);
  camio_options_add(CAMIO_OPTION_OPTIONAL, 's', "record-size", "Record size in bytes.", CAMIO_UINT64, &options.record_size, sizeof(uint64_t));
  camio_options_add(CAMIO_OPTION_FLAG, 'v', "verbose", "Produce verbose output.", CAMIO_BOOL, &options.verbose, 0);
  camio_options_long_description("Data generator for sort experiments.");
  camio_options_parse(argc, argv);
} 

uint8_t get_rand_byte() {
  uint8_t val = rand() % 256;
  return val;
} 

int main(int argc, char* argv[]) {
  configure_options(argc, argv);
  srand(time(NULL));

  camio_clock_t* clock = camio_clock_new(options.clock, NULL);
  out = camio_ostream_new(options.output, clock, NULL, NULL);

  if (options.verbose)
    printf("Generating %jd records of %jd bytes each...\n",
           options.num_records, options.record_size);

  uint64_t i, j;
  uint8_t* buf;

  for (i = 0; i < options.num_records; i++) {  
    buf = out->start_write(out, options.record_size);
    for (j = 0; j < options.record_size; j++) {
      buf[j] = get_rand_byte();
    }
    out->end_write(out, options.record_size);  
    if (i % (options.num_records / 100) == 0)  
      printf("%jd records...\n", i);
  }

  out->close(out);
}
