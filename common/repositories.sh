#!/bin/bash

## PROJECTS

aries_repositories=(
  https://github.com/hyperledger/aries.git
  https://github.com/hyperledger/aries-acapy-controllers.git
  https://github.com/hyperledger/aries-acapy-plugin-toolbox.git
  https://github.com/hyperledger/aries-cloudagent-python.git
  https://github.com/hyperledger/aries-framework-dotnet.git
  https://github.com/hyperledger/aries-framework-go.git
  https://github.com/hyperledger/aries-framework-javascript.git
  https://github.com/hyperledger/aries-mobileagent-xamarin.git
  https://github.com/hyperledger/aries-protocol-test-suite.git
  https://github.com/hyperledger/aries-rfcs.git
  https://github.com/hyperledger/aries-sdk-android.git
  https://github.com/hyperledger/aries-sdk-java.git
  https://github.com/hyperledger/aries-sdk-javascript.git
  https://github.com/hyperledger/aries-sdk-ruby.git
  https://github.com/hyperledger/aries-staticagent-python.git
  https://github.com/hyperledger/aries-toolbox.git
)

avalon_repositories=(
  https://github.com/hyperledger/avalon.git
)

besu_repositories=(
  https://github.com/hyperledger/besu.git
  https://github.com/hyperledger/besu-docs.git
  https://github.com/hyperledger/besu-native.git
  https://github.com/hyperledger/besu-permissioning-smart-contracts.git
  https://github.com/hyperledger/homebrew-besu.git
)

burrow_repositories=(
  https://github.com/hyperledger/burrow.git
)

cactus_repositories=(
  https://github.com/hyperledger/cactus.git
)

caliper_repositories=(
  https://github.com/hyperledger/caliper.git
  https://github.com/hyperledger/caliper-benchmarks.git
)

cello_repositories=(
  https://github.com/hyperledger/cello.git
  https://github.com/hyperledger/cello-analytics.git
)

explorer_repositories=(
  https://github.com/hyperledger/blockchain-explorer.git
)

fabric_repositories=(
  https://github.com/hyperledger/fabric-amcl.git
  https://github.com/hyperledger/fabric-baseimage.git
  https://github.com/hyperledger/fabric-ca.git
  https://github.com/hyperledger/fabric-chaincode-evm.git
  https://github.com/hyperledger/fabric-chaincode-go.git
  https://github.com/hyperledger/fabric-chaincode-java.git
  https://github.com/hyperledger/fabric-chaincode-node.git
  https://github.com/hyperledger/fabric-chaintool.git
  https://github.com/hyperledger/fabric-cli.git
  https://github.com/hyperledger/fabric-contract-api-go.git
  https://github.com/hyperledger/fabric-gateway-java.git
  https://github.com/hyperledger/fabric-lib-go.git
  https://github.com/hyperledger/fabric-protos-go.git
  https://github.com/hyperledger/fabric-protos.git
  https://github.com/hyperledger/fabric-rfcs.git
  https://github.com/hyperledger/fabric-samples.git
  https://github.com/hyperledger/fabric-sdk-go.git
  https://github.com/hyperledger/fabric-sdk-java.git
  https://github.com/hyperledger/fabric-sdk-node.git
  https://github.com/hyperledger/fabric-sdk-py.git
  https://github.com/hyperledger/fabric-test.git
  https://github.com/hyperledger/fabric.git
  https://github.com/hyperledger/homebrew-fabric.git
)

grid_repositories=(
  https://github.com/hyperledger/grid-contrib.git
  https://github.com/hyperledger/grid-rfcs.git
  https://github.com/hyperledger/grid-website.git
  https://github.com/hyperledger/grid.git
)

indy_repositories=(
  https://github.com/hyperledger/indy-agent.git
  https://github.com/hyperledger/indy-crypto.git
  https://github.com/hyperledger/indy-docs.git
  https://github.com/hyperledger/indy-hipe.git
  https://github.com/hyperledger/indy-jenkins-pipeline-lib.git
  https://github.com/hyperledger/indy-node.git
  https://github.com/hyperledger/indy-plenum.git
  https://github.com/hyperledger/indy-sdk.git
  https://github.com/hyperledger/indy-test-automation.git
  https://github.com/hyperledger/indy-vdr.git
)

iroha_repositories=(
  https://github.com/hyperledger/iroha-android.git
  https://github.com/hyperledger/iroha-deploy.git
  https://github.com/hyperledger/iroha-dotnet.git
  https://github.com/hyperledger/iroha-ed25519.git
  https://github.com/hyperledger/iroha-ios.git
  https://github.com/hyperledger/iroha-java.git
  https://github.com/hyperledger/iroha-javascript.git
  https://github.com/hyperledger/iroha-python.git
  https://github.com/hyperledger/iroha-scala.git
  https://github.com/hyperledger/iroha-state-migration-tool.git
  https://github.com/hyperledger/iroha-tui-client.git
  https://github.com/hyperledger/iroha.git
)

quilt_repositories=(
  https://github.com/hyperledger/quilt.git
)

sawtooth_repositories=(
  https://github.com/hyperledger/education-sawtooth-simple-supply.git
  https://github.com/hyperledger/sawtooth-ansible.git
  https://github.com/hyperledger/sawtooth-contrib.git
  https://github.com/hyperledger/sawtooth-core.git
  https://github.com/hyperledger/sawtooth-devmode.git
  https://github.com/hyperledger/sawtooth-explorer.git
  https://github.com/hyperledger/sawtooth-marketplace.git
  https://github.com/hyperledger/sawtooth-next-directory.git
  https://github.com/hyperledger/sawtooth-pbft.git
  https://github.com/hyperledger/sawtooth-poet.git
  https://github.com/hyperledger/sawtooth-raft.git
  https://github.com/hyperledger/sawtooth-rfcs.git
  https://github.com/hyperledger/sawtooth-sabre.git
  https://github.com/hyperledger/sawtooth-sdk-cxx.git
  https://github.com/hyperledger/sawtooth-sdk-dotnet.git
  https://github.com/hyperledger/sawtooth-sdk-go.git
  https://github.com/hyperledger/sawtooth-sdk-java.git
  https://github.com/hyperledger/sawtooth-sdk-javascript.git
  https://github.com/hyperledger/sawtooth-sdk-python.git
  https://github.com/hyperledger/sawtooth-sdk-rust.git
  https://github.com/hyperledger/sawtooth-sdk-swift.git
  https://github.com/hyperledger/sawtooth-seth.git
  https://github.com/hyperledger/sawtooth-supply-chain.git
  https://github.com/hyperledger/sawtooth-website.git
)

transact_repositories=(
  https://github.com/hyperledger/transact-contrib.git
  https://github.com/hyperledger/transact-rfcs.git
  https://github.com/hyperledger/transact-sdk-go.git
  https://github.com/hyperledger/transact-sdk-javascript.git
  https://github.com/hyperledger/transact.git
)

ursa_repositories=(
  https://github.com/hyperledger/ursa-docs.git
  https://github.com/hyperledger/ursa-python.git
  https://github.com/hyperledger/ursa-rfcs.git
  https://github.com/hyperledger/ursa.git
)

## LABS

labs_repositories=(
  https://github.com/hyperledger-labs/SParts.git
  https://github.com/hyperledger-labs/blockchain-analyzer.git
  https://github.com/hyperledger-labs/blockchain-automation-framework.git
  https://github.com/hyperledger-labs/blockchain-integration-framework.git
  https://github.com/hyperledger-labs/blockchain-verifier.git
  https://github.com/hyperledger-labs/byzantine-config.git
  https://github.com/hyperledger-labs/convector.git
  https://github.com/hyperledger-labs/cordentity.git
  https://github.com/hyperledger-labs/eThaler.git
  https://github.com/hyperledger-labs/ethercluster.git
  https://github.com/hyperledger-labs/fabric-block-archiving.git
  https://github.com/hyperledger-labs/fabric-chaincode-wasm.git
  https://github.com/hyperledger-labs/fabric-consortium-management.git
  https://github.com/hyperledger-labs/fabric-docs-cn.git
  https://github.com/hyperledger-labs/fabric-private-chaincode.git
  https://github.com/hyperledger-labs/hyperledger-community-management-tools.git
  https://github.com/hyperledger-labs/hyperledger-fabric-based-access-control.git
  https://github.com/hyperledger-labs/hyperledger-labs.github.io.git
  https://github.com/hyperledger-labs/inter-carrier-settlements.git
  https://github.com/hyperledger-labs/minbft.git
  https://github.com/hyperledger-labs/nephos.git
  https://github.com/hyperledger-labs/patient-consent.git
  https://github.com/hyperledger-labs/private-data-objects.git
  https://github.com/hyperledger-labs/private-transaction-families.git
  https://github.com/hyperledger-labs/sawtooth-healthcare.git
  https://github.com/hyperledger-labs/solang.git
  https://github.com/hyperledger-labs/umbra.git
)

## OTHER

other_repositories=(
  https://github.com/hyperledger/CMSIG.git
  https://github.com/hyperledger/IDWG.git
  https://github.com/hyperledger/chat-assets.git
  https://github.com/hyperledger/hyperledger-rocket-chat-hubot.git
  https://github.com/hyperledger/hyperledger.git
  https://github.com/hyperledger/hyperledger.github.io.git
  https://github.com/hyperledger/hyperledgerwp.git
  https://github.com/hyperledger/learning-materials-dev.git
  https://github.com/hyperledger/perf-and-scale-wg.git
  https://github.com/hyperledger/smart-contracts-wg.git
)

project_repositories=(
  "${aries_repositories[@]}"
  "${avalon_repositories[@]}"
  "${besu_repositories[@]}"
  "${burrow_repositories[@]}"
  "${cactus_repositories[@]}"
  "${caliper_repositories[@]}"
  "${cello_repositories[@]}"
  "${explorer_repositories[@]}"
  "${fabric_repositories[@]}"
  "${grid_repositories[@]}"
  "${indy_repositories[@]}"
  "${iroha_repositories[@]}"
  "${quilt_repositories[@]}"
  "${sawtooth_repositories[@]}"
  "${transact_repositories[@]}"
  "${ursa_repositories[@]}"
)

all_repositories=(
  "${project_repositories[@]}"
  "${labs_repositories[@]}"
  "${other_repositories[@]}"
)

# These two lines look backwards, but they are removing the pattern from the list of all repositories
github_repositories=( ${all_repositories[@]/*gerrit*/} )
