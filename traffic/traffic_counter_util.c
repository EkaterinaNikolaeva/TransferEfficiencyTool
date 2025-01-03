#include <stdio.h>
#include <pcap.h>
#include <signal.h>
#include <stdlib.h>

volatile unsigned long long total_bytes = 0;

void sigint_handler(int sig) {
    printf("%llu", total_bytes);
    exit(0);
}

void packet_handler(u_char *user_data, const struct pcap_pkthdr *pkthdr, const u_char *packet) {
    total_bytes += pkthdr->len;
}

int main(int argc, char *argv[]) {
    if (argc != 3) {
        printf("Usage: %s <interface> <port>\n", argv[0]);
        return 1;
    }
    char *iface = argv[1];
    int port = atoi(argv[2]);
    signal(SIGINT, sigint_handler);
    char errbuf[PCAP_ERRBUF_SIZE];
    pcap_t *handle = pcap_open_live(iface, BUFSIZ, 1, 1000, errbuf);
    if (handle == NULL) {
        fprintf(stderr, "Error opening device: %s\n", errbuf);
        return 1;
    }
    struct bpf_program fp;
    char filter_exp[50];
    snprintf(filter_exp, sizeof(filter_exp), "tcp port %d", port);

    if (pcap_compile(handle, &fp, filter_exp, 0, PCAP_NETMASK_UNKNOWN) == -1) {
        fprintf(stderr, "Error compiling filter: %s\n", pcap_geterr(handle));
        return 1;
    }
    if (pcap_setfilter(handle, &fp) == -1) {
        fprintf(stderr, "Error setting filter: %s\n", pcap_geterr(handle));
        return 1;
    }
    pcap_loop(handle, 0, packet_handler, NULL);
    pcap_close(handle);
    return 0;
}
