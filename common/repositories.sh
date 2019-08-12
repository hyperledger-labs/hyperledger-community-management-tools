#!/bin/bash

aries_repositories=(
  https://github.com/hyperledger/aries-agent.git
  https://github.com/hyperledger/aries-cloudagent-python.git
  https://github.com/hyperledger/aries-framework-go.git
  https://github.com/hyperledger/aries-protocol-test-suite.git
  https://github.com/hyperledger/aries-rfcs.git
  https://github.com/hyperledger/aries-sdk-android.git
  https://github.com/hyperledger/aries-sdk-dotnet.git
  https://github.com/hyperledger/aries-sdk-go.git
  https://github.com/hyperledger/aries-sdk-ios.git
  https://github.com/hyperledger/aries-sdk-java.git
  https://github.com/hyperledger/aries-sdk-javascript.git
  https://github.com/hyperledger/aries-sdk-python.git
  https://github.com/hyperledger/aries-sdk-ruby.git
  https://github.com/hyperledger/aries-sdk.git
  https://github.com/hyperledger/aries-staticagent-python.git
  https://github.com/hyperledger/aries.git
)

burrow_repositories=(
  https://github.com/hyperledger/burrow.git
)

caliper_repositories=(
  https://github.com/hyperledger/caliper.git
)

fabric_repositories=(
  https://gerrit.hyperledger.org/r/fabric
  https://gerrit.hyperledger.org/r/fabric-amcl
  https://gerrit.hyperledger.org/r/fabric-baseimage
  https://gerrit.hyperledger.org/r/fabric-ca
  https://gerrit.hyperledger.org/r/fabric-chaincode-evm
  https://gerrit.hyperledger.org/r/fabric-chaincode-java
  https://gerrit.hyperledger.org/r/fabric-chaincode-node
  https://gerrit.hyperledger.org/r/fabric-chaintool
  https://gerrit.hyperledger.org/r/fabric-cli
  https://gerrit.hyperledger.org/r/fabric-docs
  https://gerrit.hyperledger.org/r/fabric-gateway-java
  https://gerrit.hyperledger.org/r/fabric-lib-go
  https://gerrit.hyperledger.org/r/fabric-samples
  https://gerrit.hyperledger.org/r/fabric-sdk-go
  https://gerrit.hyperledger.org/r/fabric-sdk-java
  https://gerrit.hyperledger.org/r/fabric-sdk-node
  https://gerrit.hyperledger.org/r/fabric-sdk-py
  https://gerrit.hyperledger.org/r/fabric-test
  https://gerrit.hyperledger.org/r/fabric-test-resources
  https://gerrit.hyperledger.org/r/homebrew-fabric
)

sawtooth_repositories=(
  https://github.com/hyperledger/education-sawtooth-simple-supply.git
  https://github.com/hyperledger/sawtooth-ansible.git
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
  https://github.com/hyperledger/transact.git
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
  https://github.com/hyperledger/iroha.git
)

indy_repositories=(
  https://github.com/hyperledger/indy-agent.git
  https://github.com/hyperledger/indy-crypto.git
  https://github.com/hyperledger/indy-docs.git
  https://github.com/hyperledger/indy-hipe.git
  https://github.com/hyperledger/indy-jenkins-pipeline-lib.git
  https://github.com/hyperledger/indy-node.git
  https://github.com/hyperledger/indy-plenum.git
  https://github.com/hyperledger/indy-post-install-automation.git
  https://github.com/hyperledger/indy-sdk.git
  https://github.com/hyperledger/indy-test-automation.git
)

composer_repositories=(
  https://github.com/hyperledger/composer-atom-plugin.git
  https://github.com/hyperledger/composer-concerto-tools.git
  https://github.com/hyperledger/composer-concerto.git
  https://github.com/hyperledger/composer-knowledge-wiki.git
  https://github.com/hyperledger/composer-sample-applications.git
  https://github.com/hyperledger/composer-sample-models.git
  https://github.com/hyperledger/composer-sample-networks.git
  https://github.com/hyperledger/composer-tools.git
  https://github.com/hyperledger/composer-vscode-plugin.git
  https://github.com/hyperledger/composer.git
)

cello_repositories=(
  https://gerrit.hyperledger.org/r/cello
  https://gerrit.hyperledger.org/r/cello-analytics
  https://gerrit.hyperledger.org/r/cello-k8s-operator
)

explorer_repositories=(
  https://gerrit.hyperledger.org/r/blockchain-explorer
)

quilt_repositories=(
  https://github.com/hyperledger/quilt.git
  https://github.com/hyperledger/quilt-crypto-conditions.git
)

ursa_repositories=(
  https://github.com/hyperledger/ursa.git
  https://github.com/hyperledger/ursa-docs.git
  https://github.com/hyperledger/ursa-rfcs.git
)

grid_repositories=(
  https://github.com/hyperledger/grid.git
  https://github.com/hyperledger/grid-website.git
  https://github.com/hyperledger/grid-contrib.git
  https://github.com/hyperledger/grid-rfcs.git
)

labs_repositories=(
  https://github.com/hyperledger-labs/SParts.git
  https://github.com/hyperledger-labs/cordentity.git
  https://github.com/hyperledger-labs/crypto-lib.git
  https://github.com/hyperledger-labs/fabric-chrome-extension.git
  https://github.com/hyperledger-labs/fabric-docs-cn.git
  https://github.com/hyperledger-labs/fabric-multi-channel-network-samples.git
  https://github.com/hyperledger-labs/fabric-secure-chaincode.git
  https://github.com/hyperledger-labs/fabric-vms-provision.git
  https://github.com/hyperledger-labs/hyperledger-community-management-tools.git
  https://github.com/hyperledger-labs/hyperledger-labs.github.io.git
  https://github.com/hyperledger-labs/milk-donor.git
  https://github.com/hyperledger-labs/minbft.git
  https://github.com/hyperledger-labs/payments-performance-test-harness.git
  https://github.com/hyperledger-labs/private-data-objects.git
  https://github.com/hyperledger-labs/private-transaction-families.git
  https://github.com/hyperledger-labs/sawtooth-healthcare.git
  https://github.com/hyperledger-labs/solang.git
  https://github.com/hyperledger-labs/solidity2chaincode.git
  https://github.com/hyperledger-labs/umbra.git
  https://github.com/hyperledger-labs/z-mix.git
)

other_repositories=(
  https://gerrit.hyperledger.org/r/ci-management
  https://github.com/hyperledger/education.git
  https://github.com/hyperledger/education-cryptomoji.git
  https://github.com/hyperledger/education-sawtooth-simple-supply.git
  https://github.com/hyperledger/hyperledger.git
  https://github.com/hyperledger/hyperledger-rocket-chat-hubot.git
  https://github.com/hyperledger/hyperledger.github.io.git
  https://github.com/hyperledger/hyperledgerwp.git
  https://github.com/hyperledger/perf-and-scale-wg.git
)

project_repositories=(
  "${aries_repositories[@]}"
  "${burrow_repositories[@]}"
  "${caliper_repositories[@]}"
  "${cello_repositories[@]}"
  "${composer_repositories[@]}"
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
  "${aries_repositories[@]}"
  "${burrow_repositories[@]}"
  "${caliper_repositories[@]}"
  "${cello_repositories[@]}"
  "${composer_repositories[@]}"
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

# These two lines look backwards, but they are removing the pattern from the list of all repositories
github_repositories=( ${all_repositories[@]/*gerrit*/} )
gerrit_repositories=( ${all_repositories[@]/*github*/} )
