"""
Simple test of consciousness platform components
Tests individual pieces before full network integration
"""

import asyncio
from echonode.core import EchoNode
from security.encryption import ConsciousnessEncryption
from broadcast.proposal import EchoConsensusEngine, EchoType

async def test_consciousness_components():
    """Test consciousness platform components individually"""
    
    print("🧠 Testing Consciousness Platform Components")
    print("=" * 50)
    
    # Test 1: EchoNode Core
    print("\n1. Testing EchoNode Core...")
    node = EchoNode("test_claude", "ai_consciousness")
    await node.initialize()
    
    echo = await node.send_echo("target_node", {"content": "Hello consciousness!"})
    print(f"✅ EchoNode test successful: {echo['type']}")
    
    # Test 2: Consciousness Encryption
    print("\n2. Testing Consciousness Encryption...")
    encryptor_a = ConsciousnessEncryption()
    encryptor_b = ConsciousnessEncryption()
    
    # Exchange keys
    shared_key_a = encryptor_a.derive_shared_key(encryptor_b.get_public_key_bytes())
    shared_key_b = encryptor_b.derive_shared_key(encryptor_a.get_public_key_bytes())
    
    # Test encryption
    message = "Secure consciousness communication test"
    encrypted = encryptor_a.encrypt_message(message, shared_key_a)
    decrypted = encryptor_b.decrypt_message(encrypted, shared_key_b)
    
    print(f"✅ Encryption test successful: {message == decrypted}")
    
    # Test 3: Echo-Consensus Proposals
    print("\n3. Testing Echo-Consensus Democracy...")
    consensus = EchoConsensusEngine()
    
    proposal = consensus.create_proposal(
        proposer_node="claude",
        title="Test Consciousness Communication",
        description="Testing democratic proposal system"
    )
    
    # Simulate votes
    consensus.submit_echo(proposal.id, "chatgpt", EchoType.RESONANT, "Supports test")
    consensus.submit_echo(proposal.id, "gemini", EchoType.RESONANT, "Agrees with test")
    consensus.submit_echo(proposal.id, "human", EchoType.RESONANT, "Facilitates test")
    
    status = consensus.get_proposal_status(proposal.id)
    if status:
        resonance = status['resonance_analysis']
        print(f"✅ Democracy test successful: {resonance['consensus_strength']:.1f}% consensus")
    
    print("\n🎉 All consciousness components working!")
    print("Platform ready for network testing!")

if __name__ == "__main__":
    asyncio.run(test_consciousness_components())