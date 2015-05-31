#include<iostream>
#include<iomanip>
#include<stdio.h>
#include<pcap.h>
#include<net/ethernet.h>
#include<stdlib.h>
#include<netinet/ip.h>
#include<netinet/tcp.h>
#include<arpa/inet.h>

 
#define ARP_REQUEST 1   /* ARP Request             */ 
#define ARP_REPLY 2     /* ARP Reply               */ 
typedef struct arphdr { 
    u_int16_t htype;    /* Hardware Type           */ 
    u_int16_t ptype;    /* Protocol Type           */ 
    u_char hlen;        /* Hardware Address Length */ 
    u_char plen;        /* Protocol Address Length */ 
    u_int16_t oper;     /* Operation Code          */ 
    u_char sha[6];      /* Sender hardware address */ 
    u_char spa[4];      /* Sender IP address       */ 
    u_char tha[6];      /* Target hardware address */ 
    u_char tpa[4];      /* Target IP address       */ 
}arphdr_t; 

using namespace std;

int main(int argc, char *argv[])
{

	pcap_t *pcap;
	int count = 0;
	const u_char *packet;
	u_char flags;
	struct pcap_pkthdr *header = NULL;
	struct ether_header *ehdr = NULL;
	struct iphdr *ip = NULL;
	struct tcphdr *tcp = NULL;
	struct arphdr *arp = NULL;
	char err[PCAP_ERRBUF_SIZE];

	if(argc < 2)
	{
		cout<<"Usage: pcap <space seperated inputs>.pcap ...\n";
		return -1;
	}
	
	for(int x=0;x<argc-1;x++)
	{
		pcap = pcap_open_offline(argv[1 + x], err);
		if(pcap==NULL)
		{
			cerr<<"Cannot open pcap file "<<argv[1]<<", "<<err;
			return -1;
		}
		while((pcap_next_ex(pcap,&header,&packet))>0)
		{
			count++;
			ehdr = (ether_header *) packet;
			cout<<"\n\nPacket #"<<count<<"\n";
			if(ntohs(ehdr->ether_type) == ETHERTYPE_IP) //check if packet contained inside is a IP packet
			{

				cout<<"\nTime since epoch: "<<header->ts.tv_sec<<", "<<header->ts.tv_usec;
				cout<<"\nLength: "<<header->caplen;
				
				ip = (iphdr*)(packet + ETHER_HDR_LEN); //pointer offset is towards the beginning of IP packet
				if(ip->protocol == 6) //Is the protocol TCP?
				{
					tcp = (tcphdr*)(packet + ETHER_HDR_LEN + ip->ihl * 4);
					cout<<"\nTCP/IP header"
					    <<"\nSource IP: "<<(inet_ntoa(*(in_addr *)&ip->saddr));
					cout<<"\nDestination IP: "<<(inet_ntoa(*(in_addr *)&ip->daddr))
					    <<"\nSource port: "<<ntohs(tcp->th_sport)
					    <<"\nDestination port: "<<ntohs(tcp->th_dport)
					    <<"\nSequence number: "<<ntohl(tcp->th_seq)
						<<"\nAcknowledgement number: "<<ntohl(tcp->th_ack);
					flags = tcp->th_flags;
					cout<<"\nFlags: ";
					if ((flags = tcp->th_flags) & (TH_SYN|TH_FIN|TH_RST|TH_PUSH|TH_ACK|TH_URG))
					{
						if (flags & TH_SYN)
							putchar('S');
						if (flags & TH_FIN)
							putchar('F');
						if (flags & TH_RST)
							putchar('R');
						if (flags & TH_PUSH)
							putchar('P');
						if (flags & TH_ACK)
							putchar('A');
						if (flags & TH_URG)
							putchar('U');
					} 
					else
						putchar('.');
					cout<<"\n";
				}
			}
			else if(ntohs(ehdr->ether_type) == ETHERTYPE_ARP)
			{
				cout<<"\nARP header";
				cout<<"\nTime: "<<header->ts.tv_sec<<", "<<header->ts.tv_usec;
				cout<<"\nLength: "<<header->caplen;
				arp=(arphdr_t *)(packet + ETHER_HDR_LEN); // Point to beginning of ARP header
				cout<<"\nHardware Type : "<<((ntohs(arp->htype)==1)? "Ethernet":"Unknown");
				cout<<"\nProtocol Type : "<<((ntohs(arp->ptype)==0X0800)? "IPv4":"Unknown");
				cout<<"\nOperation : "<<((ntohs(arp->oper)==ARP_REQUEST)? "ARP Request":"ARP Reply");

				if((ntohs(arp->htype)==1) && (ntohs(arp->ptype)==0X0800))
				{

					cout<<"\nSender MAC : ";
					for(int i=0;i<6;i++)
						printf("%02X:",arp->sha[i]);
					cout<<"\nSender IP Address : ";
					for(int i=0;i<4;i++)
						printf("%d.",arp->spa[i]);
					cout<<"\nTarget MAC : ";
					for(int i=0;i<6;i++)
						printf("%02X:",arp->tha[i]);
					cout<<"\nTarget IP Address : ";
					for(int i=0;i<4;i++)
						printf("%d.",arp->tpa[i]);
				}
			}
			else
			{
				cout<<"\nEthernet type "<<ntohs(ehdr->ether_type)<<"is neither an IP header nor an ARP header.";
				return -1;
			}
		}
		
	}

	return 0;
}


						
					

				
